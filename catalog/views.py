from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AdvUser
from django.views.generic import CreateView
from .forms import RegisterUserForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from .forms import ApplicationForm
from .models import Application, Order, OrderItem
from .forms import OrderForm
from django.db.models import Case, When
from django.contrib.auth.decorators import user_passes_test
from .forms import ApplicationAdminForm
from .forms import DiscountForm
from django.contrib.auth import get_user_model
import uuid
from .models import DiscountCode
from decimal import Decimal
from django.contrib import messages

def index(request):
    num_application_in_work = Application.objects.filter(status__exact='o').count()
    applications = Application.objects.filter(status='d').order_by('-date')[:4]
    return render(
        request,
        'index.html',
        context={'num_application_in_work': num_application_in_work, 'applications': applications})

    orders = Order.objects.filter(user=request.user)
    return render(request, 'registration/profile.html', {
        'applications': applications,
        'orders': orders
    })


class BBLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def profile(request):
    applications = Application.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'registration/profile.html', {
        'applications': applications,
        'orders': orders
    })

class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('catalog:register_done')

class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'

@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            form.save_m2m()
            return redirect('catalog:profile')
    else:
        form = ApplicationForm()
    return render(request, 'application/create_application.html', {'form': form})


@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)

    if application.status in ['o', 'd']:
        # Сообщение, что удаление невозможно
        # Например, добавить сообщение в профиль или отобразить alert
        return redirect('catalog:profile')

    if request.method == 'POST':
        application.delete()
        # Сообщение об успешном удалении
        # Например, добавить сообщение в профиль
        return redirect('catalog:profile')

    # Отобразить форму подтверждения
    return render(request, 'application/delete_application.html', {'application': application})


@login_required
def select_services(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            applications = form.cleaned_data['applications']
            request.session['applications_ids'] = [app.id for app in applications]
            return redirect('catalog:review_order')
    else:
        form = OrderForm()
    return render(request, 'order/select_services.html', {'form': form})


@login_required
def review_order(request):
    applications_ids = request.session.get('applications_ids', [])
    applications = Application.objects.filter(id__in=applications_ids)
    ordered_applications = applications.order_by(
        Case(*[When(id=pk, then=pos) for pos, pk in enumerate(applications_ids)]),
    )

    total_price = sum(app.price for app in ordered_applications)
    discount_percent = Decimal('0')

    if request.method == 'POST':
        discount_code = request.POST.get('discount_code')
        try:
            discount = DiscountCode.objects.get(code=discount_code, user=request.user, is_used=False)
            discount_percent = discount.discount_percent
            discount.is_used = True
            discount.save()
        except DiscountCode.DoesNotExist:
            # Обработка ошибки неверного кода скидки
            pass

    discount_amount = (discount_percent / Decimal(100)) * total_price
    total_price -= discount_amount

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            discount_percent=discount_percent
        )
        for app in ordered_applications:
            OrderItem.objects.create(order=order, application=app, price=app.price)
        del request.session['applications_ids']
        return redirect('catalog:profile')

    context = {
        'applications': ordered_applications,
        'total_price': total_price,
        'discount_percent': discount_percent,
    }
    return render(request, 'order/review_order.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()
    return render(request, 'order/order_detail.html', {'order_items': order_items})

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        form = ApplicationAdminForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            if application.status == 'd' and not application.photo:
                form.add_error('photo', 'Необходимо загрузить фотографию для заявки со статусом "Выполнена"')
            elif application.status == 'o' and not application.comment:
                form.add_error('comment', 'Необходимо добавить комментарий для заявки со статусом "Принята в работу"')
            else:
                application.save()
                return redirect('catalog:profile')
    else:
        form = ApplicationAdminForm(instance=application)
    return render(request, 'application/edit_application.html', {'form': form, 'application': application})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_profile(request):
    applications = Application.objects.all()
    return render(request, 'registration/admin_profile.html', {'applications': applications})


User = get_user_model()

def assign_discount(request):
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            discount_percent = form.cleaned_data['discount_percent']
            code = str(uuid.uuid4())[:8]  # Generate a unique code
            DiscountCode.objects.create(user=user, discount_percent=discount_percent, code=code)
            messages.success(request, f'Код скидки {code} назначен пользователю {user.username}.')
            # Optionally, notify the user about the discount code
            return redirect('catalog:admin_profile')
    else:
        form = DiscountForm()
    return render(request, 'admin/assign_discount.html', {'form': form})



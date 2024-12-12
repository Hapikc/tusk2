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
from .models import Application



def index(request):
    return render(request, 'index.html')


class BBLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def profile(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'registration/profile.html', {'applications': applications})

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



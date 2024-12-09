from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AdvUser
from django.views.generic import CreateView
from .forms import RegisterUserForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView



def index(request):
    return render(request, 'index.html')


class BBLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('catalog:register_done')

class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'
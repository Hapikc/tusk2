from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    return render(request, 'index.html')


class BBLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'

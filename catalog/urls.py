from django.urls import path
from . import views
from .views import BBLoginView
from .views import profile
from .views import BBLogoutView





urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
]
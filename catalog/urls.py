from django.urls import path
from . import views
from .views import BBLoginView
from .views import profile
from .views import BBLogoutView
from .views import RegisterUserView, RegisterDoneView


app_name = 'catalog'


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),


]
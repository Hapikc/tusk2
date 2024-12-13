from django.urls import path
from . import views
from .views import BBLoginView
from .views import profile
from .views import BBLogoutView
from .views import RegisterUserView, RegisterDoneView
from .views import create_application, delete_application
from .views import select_services, review_order, order_detail


app_name = 'catalog'


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('create/', create_application, name='create_application'),
    path('delete/<int:application_id>/', delete_application, name='delete_application'),
    path('select_services/', select_services, name='select_services'),
    path('review_order/', review_order, name='review_order'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('edit_application/<int:application_id>/', views.edit_application, name='edit_application'),
    path('admin_profile/assign_discount/', views.assign_discount, name='assign_discount'),
]
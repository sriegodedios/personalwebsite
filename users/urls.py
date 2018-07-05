from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('signup/', views.registration, name='signup'),
    #path('login/', views.login, name='login'),
    path('login/', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('views/404.html', views.ajax, name='ajax'),
    path('password/change-password/', views.ResetPassword, name='Change-Password'),
    path('profile/address-info/',views.AddressPage, name='Address-Update'),
    path('profile/address-info/change',views.AddressChange, name='Address-Change'),
]

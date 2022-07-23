from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('settings/change_password/',auth_views.PasswordChangeView.as_view(template_name='accounts/changePass.html'),name='password_change'),
    path('settings/change_password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='accounts/changePassDone.html'),name='password_change_done'),

]

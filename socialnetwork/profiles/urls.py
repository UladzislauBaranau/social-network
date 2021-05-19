from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('my_profile', views.user_profile_view, name='user_profile'),
    path('edit_profile', views.edit_profile_view, name='edit_profile'),
    path('export_personal_data', views.export_personal_data_view, name='export_personal_data'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='profiles/password_reset.html'),
         name='reset_password'),

    path('reset_password_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='profiles/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'),
         name='password_reset_complete'),
]

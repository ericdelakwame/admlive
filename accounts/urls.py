from django.urls import path
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView,)
from .views import (
    register, profile, SignInView, create_profile, user_profile, UpdateUserView, moderator_request_detail, new_moderator, connect_with_user, activate_user, deactivate_user, register_student, change_password, update_profile
)
from django.urls import reverse_lazy


app_name = 'accounts'

urlpatterns = [
    path('update/profile', update_profile, name='update_profile'),
    path('change/password', change_password, name='change_password'),
    path('register/student', register_student, name='register_student'),
    path('activate/<int:user_pk>', activate_user, name='activate_user'),
    path('deactivate/<int:user_pk>', deactivate_user, name='deactivate_user'),
    path('connect/user/<int:user_pk>', connect_with_user, name='connect_user'),
    path('new/moderator/<int:user_id>', new_moderator, name='new_moderator'),
    path('moderator/request/<int:moderator_request_pk>', moderator_request_detail, name='moderator_request_detail'),
    path('user/profile/<int:user_pk>', user_profile, name='user_profile'),
    path('create/profile/<int:user_pk>', create_profile, name='create_profile'),
    path('sign/in', SignInView.as_view(), name='signin'),
    path('register/<utype>', register, name='register'),
    path('profile', profile, name='profile'),
    path('login', LoginView.as_view(
        template_name='accounts/forms/signin_form.html'), name='login'),
    path('logout', LogoutView.as_view(
        next_page='accounts:login'), name='logout'),
    path('password/change/done', PasswordChangeDoneView.as_view(template_name='accounts/registration/password_change_done.html'), name='password_change_done'),
    path('change/password', PasswordChangeView.as_view(template_name='accounts/registration/password_change_form.html', success_url=reverse_lazy('accounts:password_change_done'), extra_context={'header': 'Change Your Password'}), name='change_password'),
    path('password/reset', PasswordResetView.as_view(template_name='accounts/registration/password_reset_form.html', email_template_name='accounts/registration/password_reset_email.html',
         subject_template_name='accounts/registration/password_reset_subject.txt', success_url=reverse_lazy('accounts:password_reset_done'), extra_context={'header': 'Reset Your Password'}, from_email='support@adm.com'), name='password_reset'),

    path('password/reset/done', PasswordResetDoneView.as_view(
        template_name='accounts/registration/password_reset_done.html'), name='password_reset_done'),

    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html', success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),
    path('password/reset/complete', PasswordResetCompleteView.as_view(template_name='accounts/registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('update/<int:pk>', UpdateUserView.as_view (extra_context={
        'header': 'Update Your Details'
    }), name='update_user'),

]

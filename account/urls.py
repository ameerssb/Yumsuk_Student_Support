from django.urls import path,include
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('verify/', views.verify_code, name="verify"),
    path('reverify/', views.reverify_code, name="reverify"),
	path('profile/', include('django.contrib.auth.urls')),
	path('profile/users/',views.User_list, name='user'),
	path('profile/update/<str:username>/', views.Update_pro,name='profile_update'),
	path('profile/users/<str:username>/', views.profile,name='profile'),
    path('signin/', views.Signin.as_view(), name="Signin"),
    path('signout/', login_required(views.Signout.as_view()), name="Signout"),
    path('register/', views.Register.as_view(), name="Register"),
    path('verification/', include('verify_email.urls')),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='account/password_change.html',success_url = 'done/'),name='password_change'),    
    path('password_change/done/',auth_views.PasswordChangeView.as_view(template_name='account/password_change_done.html',success_url = 'password_change_done'),name='password_change_done'),    
    path("password_reset/", views.password_reset_request.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),      
]
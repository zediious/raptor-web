from django.urls import URLPattern, path

from raptorWeb.authprofiles import views

app_name: str = "authprofiles"

urlpatterns: list[URLPattern] = [

    # Auth
    path('html/register/', views.RegisterUser.as_view(), name="register"),
    path('html/delete/', views.RequestDeleteUser.as_view(), name="request_delete"),
    path('html/login/', views.User_Login_Form.as_view(), name="login"),
    path('oauth2/login/', views.UserLogin_OAuth.as_view(), name="login_oauth"),
    path('oauth2/login/redirect', views.UserLogin_OAuth_Success.as_view(), name="login_oauth_success"),
    path('auth/totp/setup/generate', views.GenerateTotpQr.as_view(), name="mfa_generate_qr"),
    path('auth/totp/setup/verify', views.VerifyOtpCodeSetup.as_view(), name="mfa_verify_setup"),
    path('auth/totp/setup/disable', views.DisableOtpAuth.as_view(), name="mfa_disable"),
    path('auth/totp/login', views.VerifyOtpCodeLogin.as_view(), name="mfa_login"),
    path('auth/logout/', views.user_logout, name="logout"),
    # Password Resets
    path('html/reset_password/', views.UserResetPasswordForm.as_view(), name="reset_password_form"),
    path('auth/reset_password_confirm/<str:user_reset_token>/', views.UserResetPasswordConfirm.as_view(), name="reset_password_confirm_form"),
    # Profiles
    path('html/profile/<slug:user_slug>/', views.User_Profile.as_view(), name="user_profile"),
    path('html/profile/<str:profile_name>/edit/', views.User_Profile_Edit.as_view(), name="user_profile_edit"),
    path('html/profile/', views.All_User_Profile.as_view(), name="all_user_profile"),
    path('html/profile_dropdown/', views.User_Dropdown.as_view(), name="user_dropdown"),
    # Model Deletion
    path('crud/raptorusergroup/delete/<int:pk>', views.RaptorUserGroupDelete.as_view(), name="raptorusergroup_delete"),
    path('crud/deletionqueueforuser/delete/<int:pk>', views.DeletionQueueForUserDelete.as_view(), name="deletionqueueforuser_delete")

]
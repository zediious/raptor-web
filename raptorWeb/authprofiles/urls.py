from django.urls import URLPattern, path

from raptorWeb.authprofiles import views

app_name: str = "authprofiles"

urlpatterns: list[URLPattern] = [

    # Auth
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.User_Login_Form.as_view(), name="login"),
    path('oauth2/login/', views.UserLogin_OAuth.as_view(), name="login_oauth"),
    path('oauth2/login/redirect', views.UserLogin_OAuth_Success.as_view(), name="login_oauth_success"),
    path('logout/', views.user_logout, name="logout"),
    path('accessdenied/', views.Access_Denied.as_view(), name="access_denied"),
    path('nouserfound/', views.No_User_Found.as_view(), name="no_user_found"),
    # Password Resets
    path('reset_password/', views.UserResetPasswordForm.as_view(), name="reset_password_form"),
    path('reset_password_confirm/<str:user_reset_token>', views.UserResetPasswordConfirm.as_view(), name="reset_password_confirm_form"),
    # Profiles
    path('profile/<slug:user_slug>/', views.User_Profile.as_view(), name="user_profile"),
    path('profile/<str:profile_name>/edit/', views.User_Profile_Edit.as_view(), name="user_profile_edit"),
    path('profile/', views.All_User_Profile.as_view(), name="all_user_profile"),
    path('profile_dropdown/', views.User_Dropdown.as_view(), name="user_dropdown")

]
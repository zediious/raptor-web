from django.urls import URLPattern, path

from raptorWeb.staffapps import views

app_name: str = "staffapps"

urlpatterns: list[URLPattern] = [

    path('html/all/', views.AllApps.as_view(), name="all_apps"),
    path('html/mod/', views.ModAppView.as_view(), name="mod_app"),
    path('html/admin/', views.AdminAppView.as_view(), name="admin_app"),

]

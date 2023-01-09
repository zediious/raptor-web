from django.urls import path

from staffapps import views

app_name = "staffapps"

urlpatterns = [

    path('', views.AllApps.as_view(), name="all_apps"),
    path('mod/', views.ModAppView.as_view(), name="mod_app"),
    path('admin/', views.AdminAppView.as_view(), name="admin_app"),

]

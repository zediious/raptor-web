from django.urls import path

from . import views

SR = views.ShadowRaptor

urlpatterns = [

    path('', SR.Info.home_servers, name="home"),
    path('home/', SR.Info.home_servers, name="home_alt"),
    path('rules/', SR.Info.rules, name="rules"),
    path('banneditems/', SR.Info.banned_items, name="banned_items"),
    path('applications/', SR.Info.apps, name="staff_apps"),
    path('applications/modapp/', SR.Application.mod_app, name="mod_app"),
    path('applications/adminapp/', SR.Application.admin_app, name="admin_app")

]
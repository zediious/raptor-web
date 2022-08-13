from django.contrib import admin
from django.urls import path

from . import views

SR = views.ShadowRaptor.Info

urlpatterns = [

    path('', SR.home_servers, name="home"),
    path('rules/', SR.rules, name="rules"),
    path('banneditems/', SR.banned_items, name="banned_items")

]
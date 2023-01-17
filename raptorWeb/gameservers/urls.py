from django.urls import path

from gameservers import views

app_name = "gameservers"

urlpatterns = [

    path('server_button_poll/', views.Server_Buttons.as_view(), name="server_buttons_poll"),
    path('server_button_poll_loading/', views.Server_Buttons_Loading.as_view(), name="server_buttons_poll_loading"),
    path('server_modal_poll/', views.Server_Modals.as_view(), name="server_modals_poll"),
    path('total_count_poll/', views.Total_Count.as_view(), name="totol_counts_poll")

]
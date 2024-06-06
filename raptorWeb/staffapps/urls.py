from django.urls import URLPattern, path

from raptorWeb.staffapps import views

app_name: str = "staffapps"

urlpatterns: list[URLPattern] = [

    path('html/all/', views.AllApps.as_view(), name="all_apps"),
    path('html/all/submit', views.AllAppsSubmit.as_view(), name="all_apps_submit"),
    path('html/all/approval/<int:pk>', views.AllAppsApproval.as_view(), name="all_apps_approval"),
    path('crud/submittedstaffapplication/delete/<int:pk>', views.SubmittedStaffApplicationDelete.as_view(), name="submittedstaffapplication_delete"),
    path('crud/createdstaffapplication/delete/<int:pk>', views.CreatedStaffApplicationDelete.as_view(), name="createdstaffapplication_delete"),
    path('crud/staffapplicationfield/delete/<int:pk>', views.StaffApplicationFieldDelete.as_view(), name="staffapplicationfield_delete")

]

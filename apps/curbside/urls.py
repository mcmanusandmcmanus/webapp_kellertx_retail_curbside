from django.urls import path

from .views import ArrivalAlertView, StaffDashboardView, StaffOrderStreamView

urlpatterns = [
    path("staff/dashboard/", StaffDashboardView.as_view(), name="staff_dashboard"),
    path("staff/dashboard/stream/", StaffOrderStreamView.as_view(), name="staff_dashboard_stream"),
    path("orders/<uuid:pk>/arrival/", ArrivalAlertView.as_view(), name="order_arrival"),
]

from django.urls import path

from restapi.views import *

urlpatterns = [
  path("couriers", CourierView.as_view()),
  path("couriers/<int:id>", CourierView.as_view()),
  path("orders", OrderView.as_view()),
  path("orders/assign", OrdersAssignmentView.as_view()),
  path("orders/complete", OrdersCompletionView.as_view()),
  path("couriers/<int:id>", ShowCourierView.as_view())
]

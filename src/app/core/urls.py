from django.contrib import admin
from django.urls import path
from modules.items.views import (
    buy_item_view,
    retrieve_item_view,
    success_item_payment_view,
)
from modules.orders.views import (
    buy_order_view,
    retrieve_order_view,
    success_order_payment_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("buy/<int:item_id>/", buy_item_view),
    path("item/<int:item_id>/", retrieve_item_view),
    path("item/<int:item_id>/success/", success_item_payment_view),
    path("order/<int:order_id>/", retrieve_order_view),
    path("order/<int:order_id>/buy/", buy_order_view),
    path("order/<int:order_id>/success/", success_order_payment_view),
]

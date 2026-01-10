from dataclasses import asdict

from core.container import get_container
from django.http import JsonResponse
from django.shortcuts import render
from modules.orders.use_cases.buy_order_use_case import BuyOrderUseCase
from modules.orders.use_cases.retrieve_order_use_case import RetrieveOrderUseCase

container = get_container()


def buy_order_view(request, order_id) -> JsonResponse:
    uc: BuyOrderUseCase = container.resolve(BuyOrderUseCase)

    return JsonResponse(asdict(uc.execute(order_id)))


def retrieve_order_view(request, order_id):
    uc: RetrieveOrderUseCase = container.resolve(RetrieveOrderUseCase)
    data = uc.execute(order_id)
    return render(request, "order.html", asdict(data))


def success_order_payment_view(request, order_id):
    return render(request, "order_payment_success.html", context={"id": order_id})

from dataclasses import asdict

from core.container import get_container
from django.http import JsonResponse
from django.shortcuts import render
from modules.items.use_cases.buy_item_use_case import BuyItemUseCase
from modules.items.use_cases.retrieve_item_use_case import RetrieveItemUseCase

container = get_container()


def buy_item_view(request, item_id) -> JsonResponse:
    uc: BuyItemUseCase = container.resolve(BuyItemUseCase)
    return JsonResponse(asdict(uc.execute(item_id)))


def retrieve_item_view(request, item_id):
    uc: RetrieveItemUseCase = container.resolve(RetrieveItemUseCase)
    return render(request, "item.html", asdict(uc.execute(item_id)))


def success_item_payment_view(request, item_id):
    return render(request, "item_payment_success.html", {"id": item_id})

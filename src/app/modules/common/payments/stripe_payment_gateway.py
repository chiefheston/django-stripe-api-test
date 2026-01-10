from dataclasses import dataclass
from typing import Dict

import stripe
from modules.common.payments.payment_gateway import PaymentGateway


@dataclass
class StripePaymentGateway(PaymentGateway):
    api_key: str

    def create_payment(
        self,
        amount: int,
        currency: str,
        metadata: Dict[str, str] | None = None,
    ) -> str:
        intent = stripe.PaymentIntent.create(
            api_key=self.api_key,
            amount=amount,
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={"enabled": True},
        )

        return intent.client_secret

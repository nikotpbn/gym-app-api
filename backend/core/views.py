import stripe
from uuid import uuid4
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

stripe.api_key = settings.STRIPE_API_KEY
stripe.api_version = "2025-03-31.basil"


@api_view(["POST"])
def checkout(request):
    try:
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "T-shirt"},
                        "unit_amount": 2000,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            ui_mode="custom",
            # The URL of your payment completion page
            return_url="https://example.com/return?session_id={CHECKOUT_SESSION_ID}",
        )
        return Response({"checkoutSessionClientSecret": session["client_secret"]})
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

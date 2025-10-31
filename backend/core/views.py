import stripe
from uuid import uuid4
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

stripe.api_key = settings.STRIPE_API_KEY

from gym.models import Program
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["POST"])
def register(request):
    full_name = request.data.get("full_name", None)
    email = request.data.get("email", None)
    password = request.data.get("password", None)
    password2 = request.data.get("password2", None)

    if full_name and email and password == password2:
        try:
            user = User.objects.create_user(email, password)
            customer = stripe.Customer.create(
                name=full_name,
                email=email,
            )
            user.stripe_customer_id = customer.id
            user.save()
            return Response(
                {"message": "Customer User created successfully"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"message": "Could not proceed with user creation."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response(
        {"error": "missing information"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def checkout(request):
    """
    Retrieve amount based on selected program
    would be the best practice.

    Its better to decide how much to charge on the server side,
    a trusted environment, as opposed to the client.
    """
    program_id = request.data.get("programId", None)
    currency = request.data.get("currency", None)
    try:
        program = Program.objects.get(pk=program_id)
        amount = program.price
        if program.flat_discount:
            amount -= program.flat_discount
        if program.percentage_discount:
            discount = amount * program.percentage_discount
            amount -= discount

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )
        return Response({"client_secret": intent.client_secret})
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

from django.urls import path
from core.views import checkout, register

urlpatterns = [
    path("checkout/", checkout, name="stripe-checkout"),
    path("register/", register, name="user-register"),
]

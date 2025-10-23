from django.urls import path
from core.views import checkout

urlpatterns = [path("checkout/", checkout, name="stripe-checkout")]

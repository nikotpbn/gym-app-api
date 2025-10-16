from typing import Any
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({"subscriptions": ["sub1", "sub2"]})

        return data

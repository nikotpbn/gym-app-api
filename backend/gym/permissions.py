from rest_framework.permissions import BasePermission
from rest_framework import permissions

from gym.models import Subscription


class IsSubscriberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_subscriber = request.user.subscriptions.filter(
            status="active", program=obj
        ).exists()

        return True if is_subscriber or request.user.is_staff else False

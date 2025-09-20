from rest_framework.generics import ListAPIView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from gym.models import Program
from gym.serializers import ProgramSerializer


class ProgramListCreateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        else:
            self.permission_classes = []
        return super().get_permissions()


class ProgramDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = []
        return super().get_permissions()

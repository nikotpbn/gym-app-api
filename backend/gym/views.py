from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from gym.permissions import IsSubscriberOrAdmin

from gym.models import Program, Exercise, Subscription
from gym.serializers import (
    ProgramSerializer,
    ExerciseSerializer,
    ProgramExerciseSerializer,
)


class ProgramModelViewSet(ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=True, permission_classes=[IsAuthenticated, IsSubscriberOrAdmin])
    def list_exercises(self, request, pk=None):

        obj = self.get_object()
        qs = obj.workouts.all()
        serializer = ProgramExerciseSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExerciseListCreateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAdminUser, IsAuthenticated]
        else:
            self.permission_classes = []
        return super().get_permissions()


class ExerciseDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = []
        return super().get_permissions()

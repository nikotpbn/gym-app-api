from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from gym.permissions import IsSubscriberOrAdmin

from gym.models import Program, Exercise, ProgramExercise
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

    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsAdminUser]
    )
    def exercise(self, request, pk=None):
        serializer = ProgramExerciseSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            print(serializer.errors)
            return Response(
                serializer.errors, status=status.HTTP_201_CREATED, headers=headers
            )

    @exercise.mapping.delete
    def delete_exercise(self, request, pk=None):
        wop = request.query_params.get("week_of_plan")
        dow = request.query_params.get("day_of_week")
        exercise = request.query_params.get("exercise")
        program = self.get_object()

        try:
            instance = program.workouts.get(
                week_of_plan=wop,
                day_of_week=dow,
                exercise__id=exercise,
                program=program,
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProgramExercise.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @exercise.mapping.put
    def update_exercise(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        wop = request.query_params.get("week_of_plan")
        dow = request.query_params.get("day_of_week")
        exercise = request.query_params.get("exercise")
        program = self.get_object()

        try:
            instance = program.workouts.get(
                week_of_plan=wop,
                day_of_week=dow,
                exercise__id=exercise,
                program=program,
            )

            serializer = ProgramExerciseSerializer(
                instance, data=request.data, partial=partial
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                print(request.data["program"])
                print(request.data["exercise"])
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ProgramExercise.DoesNotExist as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @exercise.mapping.patch
    def partial_update_exercise(self, request, pk=None, *args, **kwargs):
        kwargs["partial"] = True
        return self.update_exercise(request, *args, **kwargs)


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

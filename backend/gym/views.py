from django.db.models import F

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

    def get_queryset(self):
        if self.request.method == "LIST":
            user = self.request.user
            if not user.is_staff:
                return user.subscriptions.filter(status="active")
        return super().get_queryset()

    @action(
        detail=True,
        permission_classes=[IsAuthenticated, IsSubscriberOrAdmin],
        url_path="exercise/list/(?P<week_of_plan>\d)",
    )
    def list_weekly_exercises(self, request, pk=None, *args, **kwargs):
        days_list = [item[0] for item in ProgramExercise.DayOfWeekChoices.choices]
        obj = self.get_object()
        week_of_plan = kwargs["week_of_plan"]
        qs = obj.workouts.filter(week_of_plan=week_of_plan)

        response = []

        for day_of_week in days_list:
            filter = qs.filter(day_of_week=day_of_week)
            serializer = ProgramExerciseSerializer(filter, many=True)
            if serializer.data:
                response.append(
                    {"day_of_week": day_of_week, "exercises": serializer.data}
                )

        return Response(response, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsAdminUser]
    )
    def exercise(self, request, pk=None):
        request.data.update({"program": pk})
        serializer = ProgramExerciseSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

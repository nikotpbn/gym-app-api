from rest_framework.serializers import ModelSerializer

from gym.models import Program, Exercise, ProgramExercise


class ProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class ProgramExerciseSerializer(ModelSerializer):

    class Meta:
        model = ProgramExercise
        fields = "__all__"

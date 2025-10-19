from rest_framework.serializers import ModelSerializer

from gym.models import Program, Exercise, ProgramExercise


class ProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"


class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["name", "image"]


class ProgramExerciseSerializer(ModelSerializer):

    exercise = ExerciseSerializer()

    class Meta:
        model = ProgramExercise
        fields = [
            "id",
            "exercise",
            "sets",
            "reps",
            "instructions",
            "notes",
            "superset_number",
        ]

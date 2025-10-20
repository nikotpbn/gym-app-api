"""
Django custom command to seed basic initital data
"""

from django.core.management.base import BaseCommand, CommandParser
from django.core.exceptions import ObjectDoesNotExist
from gym.models import Exercise, Program, ProgramExercise

from .dataset.exercises import gym_exercises
from .dataset.programs import workout_programs
from .dataset.program_exercises import men_pro_workout


class Command(BaseCommand):
    """
    Django command to read files and populate data
    use: python manage.py seed --show [ True | False ]
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--show", type=bool, required=False, default=True)
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        """Entrypoint for command"""

        self.create_exercises(options["show"])
        self.create_program(options["show"])
        self.create_program_exercises(options["show"])

        self.stdout.write(self.style.SUCCESS("Seeding Finished!"))

    def create_program(self, show):
        """Create programs from the dataset"""
        for program in workout_programs:
            try:
                instance = Program.objects.get(name=program["name"])

                if show:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Program {instance.name} already exists, skipping creation..."
                        )
                    )

            except ObjectDoesNotExist:
                instance = Program.objects.create(**program)
                if show:
                    self.stdout.write(
                        self.style.SUCCESS(f"Creating Program Object: {instance.name}")
                    )

    def create_exercises(self, show):
        """Create exercises from the dataset"""
        for obj in gym_exercises:
            area = obj["area_of_focus"]

            # Check if the exercise already exists
            for exercise_name in obj["exercises"]:
                try:
                    instance = Exercise.objects.get(name=exercise_name)
                    if show:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Exercise {instance.name} already exists, skipping creation..."
                            )
                        )
                except ObjectDoesNotExist:
                    # Create a new exercise if it does not exist
                    exercise_obj = Exercise.objects.create(
                        area_of_focus=area, name=exercise_name
                    )
                    if show:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Creating Exercise Object: {exercise_obj.name}"
                            )
                        )

        self.stdout.write(self.style.SUCCESS("Finished seeding exercises."))

    def create_program_exercises(self, show):
        """Create program exercises from the dataset"""
        program_instance = Program.objects.get(name=men_pro_workout["program"])
        gym_workouts = men_pro_workout["GY"]["weeks"]
        home_workouts = men_pro_workout["HO"]

        for program_exercise in gym_workouts:
            data = {"program": program_instance, "environment": "GY"}
            data.update({"week_of_plan": program_exercise["week_of_plan"]})

            for day in program_exercise["days"]:
                data.update({"day_of_week": day["day_of_week"]})

                for exercise in day["exercises"]:
                    exercise_instance = Exercise.objects.get(name=exercise["name"])
                    data.update({"exercise": exercise_instance})
                    data.update({"sets": exercise["sets"]})
                    data.update({"reps": exercise["reps"]})

                    data.update(
                        {
                            "instructions": (
                                exercise["instructions"]
                                if "instructions" in exercise
                                else None
                            )
                        }
                    )
                    data.update(
                        {"notes": (exercise["notes"] if "notes" in exercise else None)}
                    )
                    data.update(
                        {
                            "superset_number": (
                                exercise["superset_number"]
                                if "superset_number" in exercise
                                else None
                            )
                        }
                    )

                    try:
                        program_exercise_instance = ProgramExercise.objects.get(
                            program=data["program"],
                            week_of_plan=data["week_of_plan"],
                            day_of_week=data["day_of_week"],
                            exercise=data["exercise"],
                        )
                        if show:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Exercise {exercise_instance.name} for {program_instance.name} on week {data["week_of_plan"]}, day {data["day_of_week"]} already exists, skipping creation..."
                                )
                            )
                    except ObjectDoesNotExist:
                        program_exercise_instance = ProgramExercise.objects.create(
                            **data
                        )
                        if show:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Creating exercise {exercise_instance.name} for {program_instance.name} on week {data["week_of_plan"]}, day {data["day_of_week"]}."
                                )
                            )

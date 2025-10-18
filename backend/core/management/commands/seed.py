"""
Django custom command to seed basic initital data
"""

from django.core.management.base import BaseCommand, CommandParser
from django.core.exceptions import ObjectDoesNotExist
from gym.models import Exercise

from .dataset.exercises import gym_exercises


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

        self.stdout.write(self.style.SUCCESS("Seeding Finished!"))

    def create_exercises(self, show):
        """Create exercises from the dataset"""
        for obj in gym_exercises:
            area = obj["area_of_focus"]

            # Check if the exercise already exists
            for exercise_name in obj["exercises"]:
                try:
                    existing_exercise = Exercise.objects.get(name=exercise_name)
                    if show:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Exercise {existing_exercise.name} already exists, skipping creation..."
                            )
                        )
                except ObjectDoesNotExist:
                    # Create a new exercise if it does not exist
                    exercise_obj = Exercise.objects.create(area_of_focus=area, name=exercise_name)
                    if show:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Creating Exercise Object: {exercise_obj.name}"
                            )
                        )

        self.stdout.write(self.style.SUCCESS("Finished seeding exercises."))

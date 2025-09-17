import pytest

from rest_framework.test import APIClient

from core.management.commands.dataset import programs, exercises, program_exercises

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def program():
    return programs.workout_programs


@pytest.fixture
def exercise():
    return exercises.gym_exercises


@pytest.fixture
def program_exercise():
    return program_exercises.men_pro_workout

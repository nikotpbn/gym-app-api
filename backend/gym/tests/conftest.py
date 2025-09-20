import pytest

from rest_framework.test import APIClient

from core.management.commands.dataset import programs, exercises, program_exercises
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def user():
    user = get_user_model().objects.create_user(
        email="test@test.com", password="testpass123"
    )
    return user


@pytest.fixture
@pytest.mark.django_db
def admin_user():
    user = get_user_model().objects.create_superuser(
        email="admin@test.com", password="adminpass123"
    )
    return user


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

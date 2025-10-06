import pytest
from decimal import Decimal
from uuid import uuid4
from datetime import datetime
from django.urls import reverse

from rest_framework import status

from gym.models import Program, Exercise, ProgramExercise, Subscription


def login_user(api_client, user, password):
    token_url = reverse("token_obtain_pair")

    response = api_client.post(token_url, {"email": user.email, "password": password})

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    return api_client


@pytest.mark.django_db
def test_program_exercise_list_endpoint_unauthenticated(
    api_client, program, exercise, program_exercise
):
    """
    Test listing all exercises of a program
    Only admin user and program subscribers should be able to list
    """
    created = 0
    [Program.objects.create(**obj) for obj in program]
    for obj in exercise:
        [
            Exercise.objects.create(area_of_focus=obj["area_of_focus"], name=name)
            for name in obj["exercises"]
        ]

    program_instance = Program.objects.get(name="Men Pro Workout")
    exercises_qs = Exercise.objects.all()

    for weeks in program_exercise["GY"]["weeks"]:

        for days in weeks["days"]:
            for exercise in days["exercises"]:
                data = {
                    "program": program_instance,
                    "environment": "GY",
                    "week_of_plan": weeks["week"],
                    "day_of_week": days["day"],
                    "exercise": exercises_qs.get(name=exercise["name"]),
                    "sets": exercise["sets"],
                    "reps": exercise["reps"],
                }

                if "instructions" in exercise:
                    data["instructions"] = exercise["instructions"]
                if "notes" in exercise:
                    data["notes"] = exercise["notes"]

                ProgramExercise.objects.create(**data)
                created += 1

    endpoint = reverse("program-list-exercises", kwargs={"pk": program_instance.pk})
    r = api_client.get(endpoint)

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_program_exercise_list_endpoint_non_subscriber_non_admin(
    api_client, program, exercise, program_exercise, user
):
    """
    Test listing all exercises of a program
    Only admin user and program subscribers should be able to list
    """
    created = 0
    [Program.objects.create(**obj) for obj in program]
    for obj in exercise:
        [
            Exercise.objects.create(area_of_focus=obj["area_of_focus"], name=name)
            for name in obj["exercises"]
        ]

    program_instance = Program.objects.get(name="Men Pro Workout")
    exercises_qs = Exercise.objects.all()

    for weeks in program_exercise["GY"]["weeks"]:

        for days in weeks["days"]:
            for exercise in days["exercises"]:
                data = {
                    "program": program_instance,
                    "environment": "GY",
                    "week_of_plan": weeks["week"],
                    "day_of_week": days["day"],
                    "exercise": exercises_qs.get(name=exercise["name"]),
                    "sets": exercise["sets"],
                    "reps": exercise["reps"],
                }

                if "instructions" in exercise:
                    data["instructions"] = exercise["instructions"]
                if "notes" in exercise:
                    data["notes"] = exercise["notes"]

                ProgramExercise.objects.create(**data)
                created += 1

    endpoint = reverse("program-list-exercises", kwargs={"pk": program_instance.pk})
    api_client = login_user(api_client, user, "testpass123")
    r = api_client.get(endpoint)

    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_program_exercise_list_endpoint_subscriber_non_admin(
    api_client, program, exercise, program_exercise, user
):
    """
    Test listing all exercises of a program
    Only admin user and program subscribers should be able to list
    """
    created = 0

    [Program.objects.create(**obj) for obj in program]
    for obj in exercise:
        [
            Exercise.objects.create(area_of_focus=obj["area_of_focus"], name=name)
            for name in obj["exercises"]
        ]

    program_instance = Program.objects.get(name="Men Pro Workout")
    exercises_qs = Exercise.objects.all()

    Subscription.objects.create(
        user=user,
        program=program_instance,
        date_joined=datetime.now(),
        amount=Decimal("50.00"),
        currency="USD",
        transaction_id=str(uuid4()),
        status="active",
        transaction_type="Credit Card",
    )

    for weeks in program_exercise["GY"]["weeks"]:

        for days in weeks["days"]:
            for exercise in days["exercises"]:
                data = {
                    "program": program_instance,
                    "environment": "GY",
                    "week_of_plan": weeks["week"],
                    "day_of_week": days["day"],
                    "exercise": exercises_qs.get(name=exercise["name"]),
                    "sets": exercise["sets"],
                    "reps": exercise["reps"],
                }

                if "instructions" in exercise:
                    data["instructions"] = exercise["instructions"]
                if "notes" in exercise:
                    data["notes"] = exercise["notes"]

                ProgramExercise.objects.create(**data)
                created += 1

    endpoint = reverse("program-list-exercises", kwargs={"pk": program_instance.pk})
    api_client = login_user(api_client, user, "testpass123")
    r = api_client.get(endpoint)

    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == created


@pytest.mark.django_db
def test_program_exercise_list_endpoint_admin(
    api_client, program, exercise, program_exercise, admin_user
):
    """
    Test listing all exercises of a program
    Only admin user and program subscribers should be able to list
    """
    created = 0

    [Program.objects.create(**obj) for obj in program]
    for obj in exercise:
        [
            Exercise.objects.create(area_of_focus=obj["area_of_focus"], name=name)
            for name in obj["exercises"]
        ]

    program_instance = Program.objects.get(name="Men Pro Workout")
    exercises_qs = Exercise.objects.all()

    for weeks in program_exercise["GY"]["weeks"]:

        for days in weeks["days"]:
            for exercise in days["exercises"]:
                data = {
                    "program": program_instance,
                    "environment": "GY",
                    "week_of_plan": weeks["week"],
                    "day_of_week": days["day"],
                    "exercise": exercises_qs.get(name=exercise["name"]),
                    "sets": exercise["sets"],
                    "reps": exercise["reps"],
                }

                if "instructions" in exercise:
                    data["instructions"] = exercise["instructions"]
                if "notes" in exercise:
                    data["notes"] = exercise["notes"]

                ProgramExercise.objects.create(**data)
                created += 1

    endpoint = reverse("program-list-exercises", kwargs={"pk": program_instance.pk})
    api_client = login_user(api_client, admin_user, "adminpass123")
    r = api_client.get(endpoint)
    assert r.status_code == status.HTTP_200_OK
    assert len(r.data) == created


# @pytest.mark.django_db
# def test_program_exercise_retrieve_unauthenticated(api_client, program, exercise):
#     """
#     Only admin user and program subscribers should be able to retrieve
#     """
#     [Program.objects.create(**obj) for obj in program]
#     for obj in exercise:
#         [
#             Exercise.objects.create(area_of_focus=obj["area_of_focus"], name=name)
#             for name in obj["exercises"]
#         ]
#     program_instance = Program.objects.get(name="Men Pro Workout")
#     exercises_instance = Exercise.objects.get(pk=1)
#     data = {
#         "program": program_instance,
#         "environment": "GY",
#         "week_of_plan": 1,
#         "day_of_week": 1,
#         "exercise": exercises_instance,
#         "sets": 3,
#         "reps": 8,
#         "instructions": "some instruction",
#         "notes": "some notes",
#     }
#     program_exercise_instance = ProgramExercise.objects.create(**data)

#     endpoint = reverse(
#         "program-exercice-detail", kwargs={"pk": program_exercise_instance.pk}
#     )
#     r = api_client.get(endpoint)

#     assert r.status_code == status.HTTP_401_UNAUTHORIZED


# @pytest.mark.django_db
# def test_program_exercise_retrieve_non_admin_non_subscriber(
#     api_client, user, program, exercise
# ):
#     """
#     Only admin user and program subscribers should be able to retrieve
#     """
#     [Program.objects.create(**obj) for obj in program]
#     for obj in exercise:
#         [
#             Exercise.objects.create(area_of_focus=obj["area_of_focus"], name=name)
#             for name in obj["exercises"]
#         ]
#     program_instance = Program.objects.get(name="Men Pro Workout")
#     exercises_instance = Exercise.objects.get(pk=1)
#     data = {
#         "program": program_instance,
#         "environment": "GY",
#         "week_of_plan": 1,
#         "day_of_week": 1,
#         "exercise": exercises_instance,
#         "sets": 3,
#         "reps": 8,
#         "instructions": "some instruction",
#         "notes": "some notes",
#     }
#     program_exercise_instance = ProgramExercise.objects.create(**data)

#     api_client = login_user(api_client, user, "testpass123")

#     endpoint = reverse("program-exercice-detail")
#     r = api_client.get(endpoint, kwargs={"pk": program_exercise_instance.pk})

#     assert r.status_code == status.HTTP_403_FORBIDDEN


# @pytest.mark.django_db
# def test_program_exercise_retrieve_subscriber_non_admin(
#     api_client, user, program, exercise
# ):
#     """
#     Only admin user and program subscribers should be able to retrieve
#     """
#     [Program.objects.create(**obj) for obj in program]
#     for obj in exercise:
#         [
#             Exercise.objects.create(area_of_focus=obj["area_of_focus"], name=name)
#             for name in obj["exercises"]
#         ]
#     program_instance = Program.objects.get(name="Men Pro Workout")
#     exercises_instance = Exercise.objects.get(pk=1)

#     Subscription.objects.create(
#         user=user,
#         program=program_instance,
#         date_joined=datetime.now(),
#         amount=Decimal("50.00"),
#         currency="USD",
#         transaction_id=str(uuid4()),
#         status="Finished",
#         transaction_type="Credit Card",
#     )

#     data = {
#         "program": program_instance,
#         "environment": "GY",
#         "week_of_plan": 1,
#         "day_of_week": 1,
#         "exercise": exercises_instance,
#         "sets": 3,
#         "reps": 8,
#         "instructions": "some instruction",
#         "notes": "some notes",
#     }
#     program_exercise_instance = ProgramExercise.objects.create(**data)

#     api_client = login_user(api_client, user, "testpass123")

#     endpoint = reverse(
#         "program-exercice-detail", kwargs={"pk": program_exercise_instance.pk}
#     )
#     r = api_client.get(endpoint)

#     assert r.status_code == status.HTTP_200_OK
#     for key, value in data.items():
#         assert key in r.data
#         assert value == r.data["key"]


# @pytest.mark.django_db
# def test_program_exercise_retrieve_admin(api_client, admin_user, program, exercise):
#     """
#     Only admin user and program subscribers should be able to retrieve
#     Admin does not need subscription
#     """
#     [Program.objects.create(**obj) for obj in program]
#     for obj in exercise:
#         [
#             Exercise.objects.create(area_of_focus=obj["area_of_focus"], name=name)
#             for name in obj["exercises"]
#         ]
#     program_instance = Program.objects.get(name="Men Pro Workout")
#     exercises_instance = Exercise.objects.get(pk=1)

#     api_client = login_user(api_client, admin_user, "adminpass123")

#     data = {
#         "program": program_instance,
#         "environment": "GY",
#         "week_of_plan": 1,
#         "day_of_week": 1,
#         "exercise": exercises_instance,
#         "sets": 3,
#         "reps": 8,
#         "instructions": "some instruction",
#         "notes": "some notes",
#     }
#     program_exercise_instance = ProgramExercise.objects.create(**data)

#     endpoint = reverse(
#         "program-exercice-detail", kwargs={"pk": program_exercise_instance.pk}
#     )
#     r = api_client.get(endpoint)

#     assert r.status_code == status.HTTP_200_OK
#     for key, value in data.items():
#         assert key in r.data
#         assert value == r.data["key"]


@pytest.mark.django_db
def test_program_exercise_create_endpoint_unauthenticated(
    api_client, program, exercise
):
    """
    Should be unauthorized for non authenticated users
    """

    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )

    data = {
        "program": program_instance.pk,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance.pk,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    r = api_client.post(endpoint, data=data)

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_program_exercise_create_endpoint_non_admin(
    api_client, program, exercise, user
):
    """
    Should be forbidden for common users
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )

    data = {
        "program": program_instance.pk,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance.pk,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    api_client = login_user(api_client, user, "testpass123")
    r = api_client.post(endpoint, data=data)

    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_program_exercise_create_endpoint_admin(
    api_client, program, exercise, admin_user
):
    """
    Only admin users can create workouts for a program
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )

    data = {
        "program": program_instance.pk,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance.pk,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    api_client = login_user(api_client, admin_user, "adminpass123")
    r = api_client.post(endpoint, data=data)

    assert r.status_code == status.HTTP_201_CREATED
    for key, value in data.items():
        assert key in r.data
        assert value == r.data[key]


@pytest.mark.django_db
def test_program_exercice_update_endpoint_unauthenticated(
    api_client, program, exercise
):
    """
    Forbidden for unauthenticated users
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )
    data = {
        "program": program_instance,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }
    ProgramExercise.objects.create(**data)

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    data["instructions"] = "updated instructions"
    r = api_client.put(endpoint, data=data)

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_program_exercice_update_endpoint_non_admin(
    api_client, program, exercise, user
):
    """
    Forbidden for non admin users
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )
    data = {
        "program": program_instance,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }
    ProgramExercise.objects.create(**data)

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    data["instructions"] = "updated instructions"
    api_client = login_user(api_client, user, "testpass123")
    r = api_client.put(endpoint, data=data)

    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_program_exercise_update_endpoint_admin(
    api_client, program, exercise, admin_user
):
    """
    Admin users are able to update
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )
    data = {
        "program": program_instance,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }
    ProgramExercise.objects.create(**data)

    # Serializer expects a pk not a instance
    data["program"] = program_instance.pk
    data["exercise"] = exercise_instance.pk

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    data["instructions"] = "updated instructions"
    api_client = login_user(api_client, admin_user, "adminpass123")
    r = api_client.put(
        endpoint + f"?week_of_plan=1&day_of_week=MON&exercise={exercise_instance.pk}",
        data=data,
    )

    assert r.status_code == status.HTTP_200_OK
    assert r.data["instructions"] == "updated instructions"


@pytest.mark.django_db
def test_program_exercice_partial_update_endpoint_unauthenticated(
    api_client, program, exercise
):
    """
    Unauthorized for unauthenticated users
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )
    data = {
        "program": program_instance,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }
    ProgramExercise.objects.create(**data)

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    r = api_client.patch(endpoint, data={"instructions": "updated instructions"})

    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_program_exercice_partial_update_endpoint_non_admin(
    api_client, program, exercise, user
):
    """
    Forbidden for non admin users
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )
    data = {
        "program": program_instance,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }
    ProgramExercise.objects.create(**data)

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    api_client = login_user(api_client, user, "testpass123")
    r = api_client.patch(endpoint, data={"instructions": "updated instructions"})

    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_program_exercise_partial_update_endpoint_admin(
    api_client, program, exercise, admin_user
):
    """
    Admin users are able to update
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )
    data = {
        "program": program_instance,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }
    ProgramExercise.objects.create(**data)

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    api_client = login_user(api_client, admin_user, "adminpass123")
    r = api_client.patch(
        endpoint + f"?week_of_plan=1&day_of_week=MON&exercise={exercise_instance.pk}",
        data={"instructions": "updated instructions"},
    )

    assert r.status_code == status.HTTP_200_OK
    assert r.data["instructions"] == "updated instructions"


@pytest.mark.django_db
def test_program_exercise_delete_endpoint_unauthenticated(
    api_client, program, exercise
):
    """
    Unauthorized for unauthenticated users
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )
    data = {
        "program": program_instance,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }
    ProgramExercise.objects.create(**data)

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    r = api_client.delete(
        endpoint + f"?week_of_plan=1&day_of_week=MON&exercise={exercise_instance.pk}"
    )
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_program_exercise_delete_endpoint_non_admin(
    api_client, program, exercise, user
):
    """
    Forbidden for non admin
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )
    data = {
        "program": program_instance,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }
    ProgramExercise.objects.create(**data)

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    api_client = login_user(api_client, user, "testpass123")
    r = api_client.delete(
        endpoint + f"?week_of_plan=1&day_of_week=MON&exercise={exercise_instance.pk}"
    )
    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_program_exercise_delete_endpoint_admin(
    api_client, program, exercise, admin_user
):
    """
    Admin users are able to delete
    """
    program_instance = Program.objects.create(**program[1])
    exercise_instance = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )
    data = {
        "program": program_instance,
        "environment": "GY",
        "week_of_plan": 1,
        "day_of_week": "MON",
        "exercise": exercise_instance,
        "sets": 3,
        "reps": 8,
        "instructions": "some instructions",
        "notes": "some notes",
    }
    ProgramExercise.objects.create(**data)

    endpoint = reverse("program-exercise", kwargs={"pk": program_instance.pk})
    api_client = login_user(api_client, admin_user, "adminpass123")
    r = api_client.delete(
        endpoint + f"?week_of_plan=1&day_of_week=MON&exercise={exercise_instance.pk}"
    )
    assert r.status_code == status.HTTP_204_NO_CONTENT

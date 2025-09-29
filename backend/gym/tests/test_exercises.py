import pytest
from gym.models import Exercise

from django.urls import reverse


@pytest.mark.django_db
def test_exercise_list_endpoint(api_client, exercise):
    """
    Test listing all exercises.
    """
    counter = 0
    for obj in exercise:
        created = [
            Exercise.objects.create(area_of_focus=obj["area_of_focus"], name=name)
            for name in obj["exercises"]
        ]
        counter += len(created)

    endpoint = reverse("exercise-list")
    r = api_client.get(endpoint)

    assert r.status_code == 200
    assert len(r.data) == counter


@pytest.mark.django_db
def test_exercise_detail_endpoint(api_client, exercise):
    """
    Test retrieving a single exercise by ID.
    """
    obj = Exercise.objects.create(
        area_of_focus=exercise[0]["area_of_focus"], name=exercise[0]["exercises"][0]
    )

    endpoint = reverse("exercise-detail", args=[obj.pk])
    r = api_client.get(endpoint)

    assert r.status_code == 200
    assert r.data["id"] == obj.id
    assert r.data["name"] == obj.name


@pytest.mark.django_db
def test_exercise_create_endpoint_unauthenticated(api_client, exercise):
    """
    Exercise creation should be unauuthorized for unauthenticated users.
    """
    new_exercise_data = exercise[0]

    endpoint = reverse("exercise-list")
    data = {
        "area_of_focus": exercise[0]["area_of_focus"],
        "name": exercise[0]["exercises"][0],
    }
    r = api_client.post(endpoint, new_exercise_data, format="json")

    assert r.status_code == 401


@pytest.mark.django_db
def test_exercise_create_endpoint_non_admin(api_client, user, exercise):
    """
    Exercise creation should be forbidden for non-admin users.
    """
    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": user.email, "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    data = {
        "area_of_focus": exercise[0]["area_of_focus"],
        "name": exercise[0]["exercises"][0],
    }

    endpoint = reverse("exercise-list")
    r = api_client.post(endpoint, data, format="json")

    assert r.status_code == 403


@pytest.mark.django_db
def test_exercise_create_endpoint_admin(api_client, admin_user, exercise):
    """
    Exercise creation should be allowed for admin users.
    """
    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": admin_user.email, "password": "adminpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    data = {
        "area_of_focus": exercise[0]["area_of_focus"],
        "name": exercise[0]["exercises"][0],
    }

    endpoint = reverse("exercise-list")
    r = api_client.post(endpoint, data, format="json")

    assert r.status_code == 201
    assert r.data["name"] == data["name"]


@pytest.mark.django_db
def test_exercise_update_endpoint_unauthenticated(api_client):
    """
    Exercise update should be unauuthorized for unauthenticated users.
    """

    data = {
        "area_of_focus": "LEG",
        "name": "Squat",
    }
    obj = Exercise.objects.create(**data)

    data = {
        "area_of_focus": "BIC",
        "name": "Hammer Curl",
    }

    endpoint = reverse("exercise-detail", kwargs={"pk": obj.pk})
    r = api_client.put(endpoint, data=data)
    assert r.status_code == 401


@pytest.mark.django_db
def test_exercise_update_endpoint_non_admin(api_client, user):
    """
    Exercise update should be forbidden for non admin users
    """
    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": user.email, "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    data = {
        "area_of_focus": "LEG",
        "name": "Squat",
    }
    obj = Exercise.objects.create(**data)

    data = {
        "area_of_focus": "BIC",
        "name": "Hammer Curl",
    }

    endpoint = reverse("exercise-detail", kwargs={"pk": obj.pk})
    r = api_client.put(endpoint, data=data)
    assert r.status_code == 403


@pytest.mark.django_db
def test_exercise_update_endpoint_admin(api_client, admin_user):
    """
    Exercise update should be permitted for admin users
    """
    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": admin_user.email, "password": "adminpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    data = {
        "area_of_focus": "LEG",
        "name": "Squat",
    }
    obj = Exercise.objects.create(**data)

    data = {
        "area_of_focus": "BIC",
        "name": "Hammer Curl",
    }

    endpoint = reverse("exercise-detail", kwargs={"pk": obj.pk})
    r = api_client.put(endpoint, data=data)
    assert r.status_code == 200
    assert r.data["area_of_focus"] == data["area_of_focus"]
    assert r.data["name"] == data["name"]


@pytest.mark.django_db
def test_exercise_partial_update_endpoint_unauthenticated(api_client):
    """
    Exercise update should be unauuthorized for unauthenticated users.
    """

    data = {
        "area_of_focus": "LEG",
        "name": "Squat",
    }
    obj = Exercise.objects.create(**data)

    data["name"] = "Leg Press"

    endpoint = reverse("exercise-detail", kwargs={"pk": obj.pk})
    r = api_client.patch(endpoint, data=data)
    assert r.status_code == 401


@pytest.mark.django_db
def test_exercise_partial_update_endpoint_non_admin(api_client, user):
    """
    Exercise update should be forbidden for non admin users
    """
    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": user.email, "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    data = {
        "area_of_focus": "LEG",
        "name": "Squat",
    }
    obj = Exercise.objects.create(**data)

    data["name"] = "Leg Press"

    endpoint = reverse("exercise-detail", kwargs={"pk": obj.pk})
    r = api_client.patch(endpoint, data=data)
    assert r.status_code == 403


@pytest.mark.django_db
def test_exercise_partial_update_endpoint_admin(api_client, admin_user):
    """
    Exercise update should be permitted for admin users
    """
    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": admin_user.email, "password": "adminpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    data = {
        "area_of_focus": "LEG",
        "name": "Squat",
    }
    obj = Exercise.objects.create(**data)

    data["name"] = "Leg Press"

    endpoint = reverse("exercise-detail", kwargs={"pk": obj.pk})
    r = api_client.patch(endpoint, data=data)
    assert r.status_code == 200
    assert r.data["name"] == data["name"]


@pytest.mark.django_db
def test_exercise_delete_endpoint_unauthenticated(api_client):
    data = {
        "area_of_focus": "LEG",
        "name": "Squat",
    }
    obj = Exercise.objects.create(**data)
    endpoint = reverse("exercise-detail", kwargs={"pk": obj.pk})
    r = api_client.delete(endpoint, data=data)
    assert r.status_code == 401


@pytest.mark.django_db
def test_exercise_delete_endpoint_non_admin(api_client, user):
    data = {
        "area_of_focus": "LEG",
        "name": "Squat",
    }
    obj = Exercise.objects.create(**data)

    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": user.email, "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    endpoint = reverse("exercise-detail", kwargs={"pk": obj.pk})
    r = api_client.delete(endpoint, data=data)
    assert r.status_code == 403


@pytest.mark.django_db
def test_exercise_delete_endpoint_admin(api_client, admin_user):
    data = {
        "area_of_focus": "LEG",
        "name": "Squat",
    }
    obj = Exercise.objects.create(**data)

    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": admin_user.email, "password": "adminpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    endpoint = reverse("exercise-detail", kwargs={"pk": obj.pk})
    r = api_client.delete(endpoint, data=data)
    assert r.status_code == 204

import pytest
from gym.models import Program

from django.urls import reverse


@pytest.mark.django_db
def test_program_list_endpoint(api_client, program):
    """
    Test listing all programs.
    """
    [Program.objects.create(**obj) for obj in program]

    endpoint = reverse("program-list")
    r = api_client.get(endpoint)

    assert r.status_code == 200
    assert len(r.data) == len(program)


@pytest.mark.django_db
def test_program_retrieve_endpoint(api_client, program):
    """
    Test retrieving individual program details.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        r = api_client.get(endpoint)

        assert r.status_code == 200
        assert r.data["name"] == prog.name


@pytest.mark.django_db
def test_program_create_endpoint_unauthenticated(api_client, program):
    """
    Program creation should be unauuthorized for unauthenticated users.
    """
    endpoint = reverse("program-list")

    for obj in program:
        r = api_client.post(endpoint, data=obj)
        assert r.status_code == 401


@pytest.mark.django_db
def test_program_create_endpoint_non_admin(api_client, user, program):
    """
    Program creation should be forbidden for non-admin users.
    """
    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": user.email, "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])
    endpoint = reverse("program-list")

    for obj in program:
        r = api_client.post(endpoint, data=obj)
        assert r.status_code == 403


@pytest.mark.django_db
def test_program_create_endpoint_admin(api_client, admin_user, program):
    """
    Program creation should be allowed for admin users.
    """
    token_url = reverse("token_obtain_pair")

    response = api_client.post(
        token_url, {"email": admin_user.email, "password": "adminpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])
    endpoint = reverse("program-list")

    for obj in program:
        r = api_client.post(endpoint, data=obj)
        assert r.status_code == 201
        assert r.data["name"] == obj["name"]
        assert r.data["training_type"] == obj["training_type"]
        assert r.data["length_in_weeks"] == obj["length_in_weeks"]
        assert r.data["price"] == str(obj["price"])
        assert r.data["currency"] == obj["currency"]
        assert r.data["flat_discount"] == str(obj["flat_discount"])
        assert r.data["percentage_discount"] == obj.get("percentage_discount", None)


@pytest.mark.django_db
def test_program_update_endpoint_unauthenticated(api_client, program):
    """
    Program update should be unauuthorized for unauthenticated users.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        data = {
            "name": "Updated Name",
            "training_type": prog.ProgramType.BODY_BUILDING,
            "length_in_weeks": prog.length_in_weeks + 1,
            "price": str(prog.price + 20),
            "currency": "EUR",
            "flat_discount": str(prog.flat_discount + 20),
        }
        r = api_client.put(endpoint, data={"name": "Updated Name"})
        assert r.status_code == 401


@pytest.mark.django_db
def test_program_partial_update_endpoint_unauthenticated(api_client, program):
    """
    Program partial update should be unauuthorized for unauthenticated users.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        data = {
            "name": "Partially Updated Name",
        }
        r = api_client.patch(endpoint, data=data)
        assert r.status_code == 401


@pytest.mark.django_db
def test_program_update_endpoint_non_admin(api_client, user, program):
    """
    Program update should be forbidden for non-admin users.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    token_url = reverse("token_obtain_pair")
    response = api_client.post(
        token_url, {"email": user.email, "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        data = {
            "name": "Updated Name",
            "training_type": prog.ProgramType.BODY_BUILDING,
            "length_in_weeks": prog.length_in_weeks + 1,
            "price": str(prog.price + 20),
            "currency": "EUR",
            "flat_discount": str(prog.flat_discount + 20),
        }
        r = api_client.put(endpoint, data=data)
        assert r.status_code == 403


@pytest.mark.django_db
def test_program_partial_update_endpoint_non_admin(api_client, user, program):
    """
    Program partial update should be forbidden for non-admin users.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    token_url = reverse("token_obtain_pair")
    response = api_client.post(
        token_url, {"email": user.email, "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        data = {
            "name": "Partially Updated Name",
        }
        r = api_client.patch(endpoint, data=data)
        assert r.status_code == 403


@pytest.mark.django_db
def test_program_update_endpoint_admin(api_client, admin_user, program):
    """
    Program update should be allowed for admin users.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    token_url = reverse("token_obtain_pair")
    response = api_client.post(
        token_url, {"email": admin_user.email, "password": "adminpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        data = {
            "name": "Updated Name",
            "training_type": prog.ProgramType.BODY_BUILDING,
            "length_in_weeks": prog.length_in_weeks + 1,
            "price": str(prog.price + 20),
            "currency": "EUR",
            "flat_discount": str(prog.flat_discount + 20),
        }
        r = api_client.put(endpoint, data=data)
        assert r.status_code == 200
        assert r.data["name"] == data["name"]
        assert r.data["training_type"] == data["training_type"]
        assert r.data["length_in_weeks"] == data["length_in_weeks"]
        assert r.data["price"] == data["price"]
        assert r.data["currency"] == data["currency"]
        assert r.data["flat_discount"] == data["flat_discount"]


@pytest.mark.django_db
def test_program_partial_update_endpoint_admin(api_client, admin_user, program):
    """
    Program partial update should be allowed for admin users.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    token_url = reverse("token_obtain_pair")
    response = api_client.post(
        token_url, {"email": admin_user.email, "password": "adminpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        data = {
            "name": "Partially Updated Name",
        }
        r = api_client.patch(endpoint, data=data)
        assert r.status_code == 200
        assert r.data["name"] == data["name"]
        assert r.data["training_type"] == prog.training_type
        assert r.data["length_in_weeks"] == prog.length_in_weeks
        assert r.data["price"] == str(prog.price)
        assert r.data["currency"] == prog.currency
        assert r.data["flat_discount"] == str(prog.flat_discount)
        assert r.data["percentage_discount"] == prog.percentage_discount


@pytest.mark.django_db
def test_program_delete_endpoint_unauthenticated(api_client, program):
    """
    Program deletion should be unauthorized for unauthenticated users.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        r = api_client.delete(endpoint)
        assert r.status_code == 401


@pytest.mark.django_db
def test_program_delete_endpoint_non_admin(api_client, user, program):
    """
    Program deletion should be forbidden for non-admin users.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    token_url = reverse("token_obtain_pair")
    response = api_client.post(
        token_url, {"email": user.email, "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        r = api_client.delete(endpoint)
        assert r.status_code == 403


@pytest.mark.django_db
def test_program_delete_endpoint_admin(api_client, admin_user, program):
    """
    Program deletion should be allowed for admin users.
    """
    created_programs = [Program.objects.create(**obj) for obj in program]

    token_url = reverse("token_obtain_pair")
    response = api_client.post(
        token_url, {"email": admin_user.email, "password": "adminpass123"}
    )

    assert response.status_code == 200
    assert "access" in response.data

    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    for prog in created_programs:
        endpoint = reverse("program-detail", kwargs={"pk": prog.pk})
        r = api_client.delete(endpoint)
        assert r.status_code == 204
        assert Program.objects.filter(pk=prog.pk).count() == 0

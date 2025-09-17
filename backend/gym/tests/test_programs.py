import pytest
from gym.models import Program

from django.urls import reverse



@pytest.mark.django_db
def test_program_endpoint(client, program):
    for obj in program:
        Program.objects.create(**obj)

    endpoint = reverse('program-list')
    r = client.get(endpoint)

    assert r.status_code == 200
    assert len(r.data) == len(program)
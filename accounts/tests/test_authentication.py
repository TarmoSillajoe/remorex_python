import pytest
from django.test import Client
from django.urls import reverse, reverse_lazy

from accounts.models import CustomUser


def test_an_admin_view(admin_client):
    response = admin_client.get("/admin/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_success(client: Client):
    user: CustomUser = CustomUser(
        username="tarmo",
        password="tarmo",
    )
    login_url = reverse_lazy("login")
    login_data = {
        "username": user.username,
        "password": user.password,
    }
    response = client.post(login_url, login_data, follow=True)
    response.client.get("/admin", data=response.cookies)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_fail(client: Client):
    login_url = reverse_lazy("login")
    login_data = {"username": "some_dude", "password": "we_cool_now?"}
    response = client.post(login_url, login_data, follow=True)
    response = client.get("/admin", data=response.cookies)
    assert response.status_code != 200

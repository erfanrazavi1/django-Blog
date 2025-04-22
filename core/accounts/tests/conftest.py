from accounts.models import CustomUser
import pytest


@pytest.fixture
def registration_data():
    return {
        "email": "erfan6235@gmail.com",
        "phone": "09123456789",
        "password": "hasaniii1234",
        "confirm_password": "hasaniii1234",
    }


@pytest.fixture
def login_data():
    return {
        "email": "erfan6235@gmail.com",
        "password": "hasaniii1234",
    }


@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        email="erfan6235@gmail.com",
        phone="09123456789",
        password="hasaniii1234",
        is_verified=True,
        is_staff=True,
    )

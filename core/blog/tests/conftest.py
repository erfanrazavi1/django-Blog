from accounts.models import CustomUser
from django.contrib.auth.models import Permission
from blog.models import Category, Post
import pytest


@pytest.fixture
def user(db):
    user = CustomUser.objects.create_user(
        email="erfan6235@gmail.com",
        phone="09123456789",
        password="123456789",
        is_staff=True,
    )
    permission = Permission.objects.get(codename="add_post")
    user.user_permissions.add(permission)

    return user


@pytest.fixture
def profile(user):
    profile = user.profile
    return profile


@pytest.fixture
def category(db):
    category = Category.objects.create(name="Test Category")
    return category


@pytest.fixture
def post(db, profile, category):
    post = Post.objects.create(
        author=profile,
        title="Test Title",
        content="Test Content",
        status=True,
        category=category,
    )
    return post


@pytest.fixture
def data(db, profile, category):
    data = {
        "author": profile,
        "title": "Test Title",
        "content": "Test Content",
        "status": True,
        "category": category,
    }
    return data

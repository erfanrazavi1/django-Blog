from rest_framework.test import APIClient
from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestPostApi:
    """
    Test suite for Blog Post API endpoints.

    This test class uses Django REST framework's APIClient to test various
    HTTP interactions with the Post endpoints under different conditions,
    such as authentication and input validation.

    Fixtures used:
    - `user`: A test user instance, used to simulate authenticated requests.
    - `profile`: A profile instance associated with the user.
    - `category`: A category instance used to classify posts.
    - `data`: A dictionary containing valid post creation data.
    - `post`: A pre-created post instance for detail view tests.

    Test Coverage:
    - GET /posts/            : Verify 200 OK status for retrieving post list.
    - GET /posts/{id}/       : Verify 200 OK status for retrieving post detail.
    - POST /posts/ (unauth)  : Ensure 401 Unauthorized response when not logged in.
    - POST /posts/ (auth)    : Ensure 201 Created for valid post creation by an authenticated user.
    - POST /posts/ (invalid) : Ensure 400 Bad Request for missing/invalid required fields.
    """

    client = APIClient()

    def test_get_post_list_resolve_status_200(self):

        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_post_detail_resolve_status_200(self, post):
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.pk})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self, data):
        url = reverse("blog:api-v1:post-list")
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_201_status(self, user, data):

        url = reverse("blog:api-v1:post-list")
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_create_post_response_invalid_data_400_status(self, user, profile):

        url = reverse("blog:api-v1:post-list")
        self.client.force_authenticate(user=user)
        data = {
            "author": profile,
            "title": "Test Title",
        }
        response = self.client.post(url, data)
        assert response.status_code == 400

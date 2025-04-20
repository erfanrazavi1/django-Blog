from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import CustomUser
import pytest

@pytest.mark.django_db
class TestUserApi:
    """
    This class contains a series of tests designed to verify the functionality of the user registration, login, 
    and logout API endpoints. The test cases cover common scenarios for creating, logging in, and logging out users, 
    as well as handling edge cases like duplicate emails, incorrect passwords, and missing data.

    Each test method performs a specific task, sends an HTTP request to the respective API endpoint using the 
    APIClient, and checks if the returned response matches the expected behavior.

    The test methods included are:
    1. `test_register_user_response_status_201`: Verifies that a user can register successfully.
    2. `test_duplicate_email_response_status_400`: Verifies that the system returns an error when attempting 
       to register with a duplicate email.
    3. `test_login_user_response_status_200`: Verifies that a user can log in with correct credentials.
    4. `test_login_user_wrong_password_response_status_400`: Verifies that login fails with incorrect passwords.
    5. `test_register_user_with_mismatched_passwords_response_status_400`: Verifies that registration fails 
       if the passwords do not match.
    6. `test_user_logout_response_status_204`: Verifies that a user can log out successfully.
    7. `test_register_missing_email_response_400`: Verifies that the registration request fails if the email is missing.

    Fixtures used in the tests:
    - `registration_data`: Provides a dictionary with the required data for registering a user (email, password, etc.).
    - `login_data`: Provides a dictionary with the login credentials (email and password) for user authentication.
    - `user`: A fixture that creates and returns a user instance in the database, which is used to simulate 
      the login process in certain test cases.
    
    The tests use the `APIClient` to send HTTP requests to the registration, login, and logout API endpoints and 
    then assert the response status codes and the data returned from the server to ensure everything functions 
    as expected.
    """

    client = APIClient()

    def test_register_user_response_status_201(self, registration_data):
        """
        Test the successful registration of a new user. The test checks that:
        - The user is registered successfully (HTTP status code 201).
        - The response data contains the user's email and a success message.
        """
        url = reverse("accounts:accounts-api-v1:registration")
        response = self.client.post(url, registration_data)
        assert response.status_code == 201
        assert response.data["email"] == "erfan6235@gmail.com"
        assert response.data["detail"] == "User registered successfully"
        
    def test_duplicate_email_response_status_400(self, registration_data):
        """
        Test the registration with a duplicate email. The test checks that:
        - The system returns an error (HTTP status code 400) when trying to register with an email that already exists.
        """
        url = reverse("accounts:accounts-api-v1:registration")
        self.client.post(url, registration_data)
        response = self.client.post(url, registration_data)
        assert response.status_code == 400

    def test_login_user_response_status_200(self, login_data, registration_data, user):
        """
        Test the successful login of a user. The test checks that:
        - The login is successful (HTTP status code 200).
        - The response data contains the logged-in user's email.
        """
        registration_url = reverse("accounts:accounts-api-v1:registration")
        login_url = reverse("accounts:accounts-api-v1:token-login")

        self.client.post(registration_url, registration_data)
        
        response = self.client.post(login_url, login_data)

        assert response.status_code == 200
        assert response.data["email"] == "erfan6235@gmail.com"

    def test_login_user_wrong_password_response_status_400(self, login_data, registration_data):
        """
        Test the login with a wrong password. The test checks that:
        - The login fails (HTTP status code 400) when an incorrect password is provided.
        """
        url = reverse("accounts:accounts-api-v1:token-login")
        self.client.post(url, registration_data)
        login_data["password"] = "wrongpassword" # real password is "hasaniii1234"
        response = self.client.post(url, login_data)
        assert response.status_code == 400
    
    def test_register_user_with_mismatched_passwords_response_status_400(self, registration_data):
        """
        Test the registration with mismatched passwords. The test checks that:
        - The registration fails (HTTP status code 400) when the password and confirm_password do not match.
        """
        url = reverse("accounts:accounts-api-v1:registration")
        registration_data["confirm_password"] = "wrongpassword" # real password is "hasaniii1234"
        response = self.client.post(url, registration_data)
        assert response.status_code == 400
    
    def test_user_logout_response_status_204(self, login_data, registration_data, user):
        """
        Test the successful logout of a user. The test checks that:
        - The logout is successful (HTTP status code 204) after the user has logged in.
        """
        registration_url = reverse("accounts:accounts-api-v1:registration")
        login_url = reverse("accounts:accounts-api-v1:token-login")
        logout_url = reverse("accounts:accounts-api-v1:token-logout")

        self.client.post(registration_url, registration_data)
        
        
        login_response = self.client.post(login_url, login_data)
        token = login_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        logout_response = self.client.post(logout_url)
        assert logout_response.status_code == 204

    def test_register_missing_email_response_400(self, registration_data):
        """
        Test the registration with missing email. The test checks that:
        - The registration fails (HTTP status code 400) if the email field is left empty.
        """
        self.client.credentials() # Clear any existing credentials
        url = reverse("accounts:accounts-api-v1:registration")
        registration_data["email"] = ""
        response = self.client.post(url, registration_data)
        assert response.status_code == 400

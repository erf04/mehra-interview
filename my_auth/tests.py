from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken

class AuthAPITestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing purposes
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.url_register = "/api/token/register/" 
        cls.url_login = "/api/token/"  
        cls.url_refresh = "/api/token/refresh/"  
    
    def test_user_registration(self):
        """
        Test that a new user can register successfully.
        """
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com"
        }
        
        response = self.client.post(self.url_register, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    
    def test_user_login(self):
        """
        Test that a user can log in and receive a valid JWT token.
        """
        data = {
            "username": "testuser",
            "password": "password123"
        }
        
        response = self.client.post(self.url_login, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Check if the response contains the access token


    def test_refresh_token(self):
        """
        Test that a user can refresh their JWT token.
        """
        token = RefreshToken.for_user(self.user)
        data = {
            "refresh": str(token)
        }
        
        response = self.client.post(self.url_refresh, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Check if the response contains the access token

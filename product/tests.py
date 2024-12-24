from rest_framework.test import APITestCase
from rest_framework import status
from my_auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import Product

class ProductAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create the owner user and a non-owner user
        cls.owner = User.objects.create_user(username="owner", password="password123")
        cls.non_owner = User.objects.create_user(username="non_owner", password="password456")
        
        # Generate JWT tokens for both users
        cls.owner_token = str(AccessToken.for_user(cls.owner))
        cls.non_owner_token = str(AccessToken.for_user(cls.non_owner))
        cls.product = Product.objects.create(
            name="Test Product",
            price=100,
            description="A test product",
            created_by=cls.owner
        )


    def test_access_with_jwt(self):
        """
        Test that access to product APIs is allowed with valid JWT.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')

        # Test GET product list with JWT
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test POST create product with JWT
        response = self.client.post('/api/products/', data={
            "name": "New Product",
            "price": 50.0,
            "description": "Another test product"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test GET one product with JWT
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test PUT update product with JWT
        response = self.client.put(f'/api/products/{self.product.id}/', data={
            "name": "Updated Product",
            "price": 150.0,
            "description": "Updated description"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test DELETE product with JWT
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_access_products_without_jwt(self):

        # Test GET product list without JWT
        response = self.client.get('/api/products/') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test POST create product without JWT
        response = self.client.post('/api/products/', data={
            "name": "New Product",
            "price": 50,
            "description": "Another test product"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


        # Test GET one product by id without JWT
        response = self.client.get(f'/api/products/{self.product.id}/') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test PUT update product without JWT
        response = self.client.put(f'/api/products/{self.product.id}/', data={
            "name": "Updated Product",
            "price": 150,
            "description": "Updated description"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test DELETE product without JWT
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_and_delete_product_as_non_owner(self):

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.non_owner_token}')
        # update part 
        response = self.client.put(f'/api/products/{self.product.id}/', data={
            "name": "Updated Product",
            "price": 150.0,
            "description": "Updated description"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expect Forbidden


        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.non_owner_token}')
        # delete part
        response = self.client.delete(f'/api/products/{self.product.id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expect Forbidden


    def test_get_or_update_or_delete_product_with_not_exist_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')

        # Test GET non-existent product
        response = self.client.get('/api/products/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test PUT non-existent product
        response = self.client.put('/api/products/999/', data={
            "name": "Updated Product",
            "price": 150.0,
            "description": "Updated description"
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test DELETE non-existent product
        response = self.client.delete('/api/products/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_product_with_repetitive_name(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.non_owner_token}')

        # Test POST create product with repetitive name
        response = self.client.post('/api/products/', data={
            "name": "Test Product",
            "price": 50.0,
            "description": "Another test product"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_product_with_negative_price(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.non_owner_token}')

        # Test POST create product with negative price
        response = self.client.post('/api/products/', data={
            "name": "Test Product",
            "price": -50.0,
            "description": "Another test product"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



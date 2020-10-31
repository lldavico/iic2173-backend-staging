from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class Tests(APITestCase):

    HOST = "http://localhost:8000"
    urls = {
        "get_boards": "/api/boards/get_boards",
        "create_user": "/api/users/create_user",
        "get_board_thread_404": "/api/threads/get_board_threads/1",
    }

    def test_get_boards(self):

        url = f'{self.HOST}{self.urls["get_boards"]}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_existent_board(self):

        url = f'{self.HOST}{self.urls["get_board_thread_404"]}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_users(self):
        
        url = f'{self.HOST}{self.urls["create_user"]}'

        user_data = {
            "firstName": "tester",
            "lastName": "iic2173",
            "username": "hola",
            "password": "123456789",
            "email": "test@uc.cl"
        }

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
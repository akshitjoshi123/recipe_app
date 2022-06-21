import email
from telnetlib import SE
from urllib import response
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)



class UserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    
    def test_create_valid_user_success(self):
        payload = {
            'email': 'akshit123@gamil.com',
            'password': 'akshit12345',
            'name': 'Akshit Joshi'

        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        payload = {'email': 'akshit123@gamil.com','password': 'akshit12345'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test for password must be more then 5 characters"""
        payload = {'email': 'akshit123@gamil.com','password': 'ak'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        payload = {'email': 'akshit123@gamil.com','password': 'akshit12345'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(email='akshit123@gamil.com',password='akshit12345')
        payload = {'email': 'akshit123@gamil.com','password': 'wrongpassword'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.data.get('non_field_errors')[0], 'Unable to authenication with this credentials')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {'email': 'akshit123@gamil.com','password': 'akshit12345'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.data.get('non_field_errors')[0], 'Unable to authenication with this credentials')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertEqual(res.data.get('password')[0], 'This field may not be blank.')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
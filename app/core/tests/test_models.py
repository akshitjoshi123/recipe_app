import email
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_sccessful(self):
        """Test create new user with sccessful email"""
        email = "test@gmail.com"
        password = "Testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the new user email with normalized"""
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_with_invalid_email(self):
        """Test of create new user with no email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')


    def test_create_new_superuser(self):
        """Test of creating new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@gmail.com",
            "testpass123"
        )
        
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)



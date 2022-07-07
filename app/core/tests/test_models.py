import email
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password='Testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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


    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Vegan'
        )
        self.assertEqual(str(tag), tag.name)


    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = 'Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)


    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title = 'Tometo sauce',
            time_minutes = 5,
            price = 50.00,
        )
        self.assertEqual(str(recipe.title), recipe.title)


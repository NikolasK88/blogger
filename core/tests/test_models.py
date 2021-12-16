from django.test import TestCase
from django.contrib.auth import get_user_model


def sample_user(email='test@gmail.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)



class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test that creates user with email and pass"""
        email = 'blogger@gmail.com'
        password = '1qazxsw2'

        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email for a new user is normolized"""

        email = 'blogger@GMAIL.com'
        password = '1qazxsw2'

        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email.lower())

    def test_creating_user_without_email(self):
        """Test that gives an error for creating user without the password"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '1qazxsw2')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            '1qazxsw2'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

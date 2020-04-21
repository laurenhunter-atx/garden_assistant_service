from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import APIClient
from accounts.models import User


class AccountsManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='normal.user', email='normal@user.com', password='foo',
            city='austin', state='tx', zip='78759'
        )
        self.assertEqual(user.username, 'normal.user')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.city, 'austin')
        self.assertEqual(user.state, 'tx')
        self.assertEqual(user.zip, '78759')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', username='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super.user', 'super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'super.user')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class AccountsTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/auth/', include('accounts.api.urls'))
    ]

    def test_create_account(self):
        data = {
            'username': 'lauren.hunter', 'email': 'lh@mail.com',
            'password': '123', 'name': 'lauren',
            'city': 'Austin', 'state': 'tx', 'zip': '78723'
        }
        response = self.client.post('/api/auth/register', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'lauren')

    def test_login_account(self):
        # create account
        register = {
            'username': 'lauren.hunter', 'email': 'lh@mail.com',
            'password': '123', 'name': 'lauren',
            'city': 'Austin', 'state': 'tx', 'zip': '78723'
        }
        self.client.post('/api/auth/register', register, format='json')

        # then login
        login = {
            'username': 'lauren.hunter',
            'password': '123'
        }
        response = self.client.post('/api/auth/login', login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'lauren.hunter')
        self.assertTrue(response.data['token'])

    def test_get_account(self):
        # create account and login
        register = {
            'username': 'lauren.hunter', 'email': 'lh@mail.com',
            'password': '123', 'name': 'lauren',
            'city': 'Austin', 'state': 'tx', 'zip': '78723'
        }
        self.client.post('/api/auth/register', register, format='json')
        response = self.client.post('/api/auth/login', {'username': 'lauren.hunter', 'password': '123'}, format='json')
        token = response.data['token']
        print(token)

        # then fetch account
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get('/api/auth/user')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'lauren.hunter')
        self.assertEqual(response.data['email'], 'lh@mail.com')
        self.assertEqual(response.data['name'], 'lauren')
        self.assertEqual(response.data['city'], 'Austin')
        self.assertEqual(response.data['state'], 'tx')
        self.assertEqual(response.data['zip'], '78723')

from rest_framework.test import APITestCase
from django.urls import include, path
from rest_framework import status


class PlantsTests(APITestCase):
    urlpatterns = [
        path('api/auth/', include('accounts.api.urls')),
        path('api/', include('plants.urls'))
    ]

    def setUp(self):
        register = {
            'username': 'lauren.hunter', 'email': 'lh@mail.com',
            'password': '123', 'name': 'lauren',
            'city': 'Austin', 'state': 'tx', 'zip': '78723'
        }
        self.client.post('/api/auth/register', register, format='json')
        response = self.client.post('/api/auth/login', {'username': 'lauren.hunter', 'password': '123'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_create_get_plant(self):
        data = {'name': 'watermelon'}
        response = self.client.post('/api/plants/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/plants/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plants = response.data
        self.assertEqual(plants[0]['name'], 'watermelon')

        response = self.client.get('/api/plants/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

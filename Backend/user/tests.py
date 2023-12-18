from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import *

# Create your tests here.
class TestLogin(APITestCase):

    def authenticate(self):
        url = reverse('registerUser')
        c=User.objects.all().count()
        data={"first_name":"test1","last_name":"t","email":"test12@gmail.com","password":"12345","type":"customer"}
        response = self.client.post(url, data, format='json')
        print(response.data['info']['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.all().count(),c+1)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['info']['token']}")

    def test_create_location_object(self):
        #self.authenticate()
        url=reverse('createLocation')
        data={"name":"Kelvin","address":"NE16"}
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(Location.objects.get().name,'Kelvin')

    """
    def test_get_location(self):
        url = reverse('getBikesPerLocation',kwargs={'pk':1})
        response = self.client.get(url)
        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #print(response.data["token"])
    
    """
    def test_update_location_object(self):
        url = reverse('updateCustomerDetails',args=[2])
        data={"first_name":"test1","last_name":"t","email":"test12@gmail.com","password":"12345","type":"customer"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
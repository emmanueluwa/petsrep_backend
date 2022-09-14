from django.test import TestCase
from rest_framework import status 
from rest_framework.test import APITestCase
from members.models import Profile, Animal
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class ProfileTests(APITestCase):

    def test_view_posts(self):
        url = reverse('members_api:listcreate')
        #setting up the response
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def create_profile(self):
        self.test_animal = Animal.objects.create(name='staff')

        self.test_user1 = User.objects.create_user(
            username='wise_ngu', password='101101101'
        )

        data = {
            "bio": "ngu", "member": 1, "location": "ngu city" 
        }
    
        url = reverse('members_api:listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

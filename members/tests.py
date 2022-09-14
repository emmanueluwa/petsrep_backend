from unicodedata import category
from django.test import TestCase
from django.contrib.auth.models import User
from members.models import Profile, Animal

# Create your tests here.
class Tests_Create_Profile(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_animal = Animal.objects.create(name="Akita")
        testuser1 = User.objects.create_user(
            username='wise_ngu', password='101101101'
        )
        test_profile = Profile.objects.create(
            animal_id='1',
            member_id = '1',
            bio = 'bio ngu',
            location = 'ngu city',
            status = 'active'
        )

    def test_profile_content(self):
        profile = Profile.profileobjects.get(id=1)
        ani = Animal.objects.get(id=1)
        member = f'{profile.member}'
        bio = f'{profile.bio}'
        location = f'{profile.location}'
        status = f'{profile.status}'
        self.assertEqual(member, 'wise_ngu')
        self.assertEqual(bio, 'bio ngu')
        self.assertEqual(location, 'ngu city')
        self.assertEqual(status, 'active')
        self.assertEqual(str(profile), 'wise_ngu')
        self.assertEqual(str(ani), 'Akita')







        
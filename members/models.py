from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Animal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
  #only show active profiles
    class ProfileObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='active')

  #only show active profiles
    options = (
        ('hidden', 'Hidden'),
        ('active', 'Active')
    )

    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, default=1)
    member = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    display_image = models.ImageField(upload_to='display_images', default='default_butterfly.jpg')
    location = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=options, default='active')
    #default manager
    objects = models.Manager()
    #customer manager
    profileobjects = ProfileObjects()
    

    def __str__(self):
      return f'Profile of {self.member.username}'


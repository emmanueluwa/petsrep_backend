from django.contrib import admin
from . import models 

# Register your models here.
@admin.register(models.Profile)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('member', 'id', 'status')


admin.site.register(models.Animal)

from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Blog),
admin.site.register(models.Post),
admin.site.register(models.Profil),
admin.site.register(models.Komentarz)

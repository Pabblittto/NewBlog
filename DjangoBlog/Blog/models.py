from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Blog(models.Model):
    IDBlog=models.IntegerField(primary_key=True)
    Nazwa=models.CharField(max_length=128)
    IDAutor=models.ForeignKey(User,on_delete=models.CASCADE)

class Post(models.Model):
    IDPost=models.IntegerField(primary_key=True)
    Tytul=models.CharField(max_length=128)
    Tresc=models.TextField()
    Data=models.DateTimeField(default=timezone.now)
    IDBlog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    Haslo=models.CharField(max_length=8)
    Obraz=models.ImageField(upload_to='Obrazki')

class Uzytkownik(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True) #dziedziczenie pola z wbudowanej tabeli User
    Zdjecie=models.ImageField(default='domyslny_obrazek.jpg',upload_to='Obrazki')
    Opis=models.CharField(max_length=1000)

class Komentarz(models.Model):
    IDKomentarz=models.IntegerField(primary_key=True)
    IDUzytkownik=models.ForeignKey(User,on_delete=models.CASCADE)
    IDPost=models.ForeignKey(Post,on_delete=models.CASCADE)
    Data=models.DateTimeField(default=timezone.now)
    Tresc=models.TextField()
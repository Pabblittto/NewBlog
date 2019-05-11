from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
import os
from PIL import Image

def path_and_rename(instance,filename):# funkcja dla profilu aby zmieniac nazwe przychodzacego pliikku
    path='Profilowe/'
    ext=filename.split('.')
    name=instance.User.username+'.'+ext[-1]
    return os.path.join(path,name)
# Create your models here.
class Blog(models.Model):
    IDBlog=models.AutoField(primary_key=True)
    Nazwa=models.CharField(max_length=128)
    IDAutor=models.ForeignKey(User,on_delete=models.CASCADE)

class Post(models.Model):
    IDPost=models.AutoField(primary_key=True)
    Tytul=models.CharField(max_length=128)
    Tresc=models.TextField()
    Data=models.DateTimeField(default=timezone.now)
    IDBlog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    Haslo=models.CharField(max_length=8,blank=True)
    Obraz=models.ImageField(upload_to='Obrazki',blank=True)

class Profil(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    Zdjecie=models.ImageField(default='Profilowe/default_pic.jpg',upload_to=path_and_rename)
    Opis=models.CharField(max_length=1000,blank=True)
    #to cos wczesniej dzialalo ale z dziwnych czesci wycinalo a potem wypierdala ze nie przyjelo obrazka
    #def save(self):
       # super().save()
       # temp=Image.open(self.Zdjecie.path)
       # if temp.height>500 or temp.width>500:
        #    width,height=get_image_dimensions(temp)
       #     temp = temp.crop((height/2-500, width/2-500, width, height))
       #     temp=temp.resize((500, 500), Image.ANTIALIAS)
       # temp.save(self.Zdjecie.path)
    #to powinno reskalowac obraz, wartosci do zmian
    #def save(self):
     #   super().save()
      #  temp=Image.open(self.Zdjecie.path)
       # if temp.height>500 or temp.width>500:
        #    output_size=(500,500)
         #   temp.thumbnail(output_size)
          #  temp.save(self.Zdjecie.path) # to działa ale nie wycina środka tylko zmiensza rozdzielczośc obrazka~ Paweł


class Komentarz(models.Model):
    IDKomentarz=models.AutoField(primary_key=True)
    IDUzytkownik=models.ForeignKey(User,on_delete=models.CASCADE)
    IDPost=models.ForeignKey(Post,on_delete=models.CASCADE)
    Data=models.DateTimeField(default=timezone.now)
    Tresc=models.TextField()


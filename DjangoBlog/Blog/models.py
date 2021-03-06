from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django import forms
from django.core.files.images import get_image_dimensions
from django.core.files import File
import os
from PIL import Image

def path_and_rename(instance,filename):# funkcja dla profilu aby zmieniac nazwe przychodzacego pliikku
    path='Profilowe/'
    ext=filename.split('.')
    name=instance.User.username+'.'+ext[-1]
    return os.path.join(path,name)

def path_and_renamePost(instance,filename):# funkcja dla profilu aby zmieniac nazwe przychodzacego pliikku
    path='Obrazki/'
    ext=filename.split('.')
    name='Blog'+str(instance.IDBlog.IDBlog)+'Post'+ str(instance.IDPost)+'.'+ext[-1]
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
    Obraz=models.ImageField(upload_to=path_and_renamePost,default='Obrazki/default_pic.jpg',blank=True)

class Profil(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    Zdjecie=models.ImageField(default='Profilowe/default_pic.jpg',upload_to=path_and_rename)
    Opis=models.CharField(max_length=1000,blank=True)
    #to cos dziala ale w dziwny sposob przycina z przesunieciem
    def save(self,force_insert=False, force_update=False, using=None):
        super().save()
        temp=Image.open(self.Zdjecie.path)
        if temp.height>500 or temp.width>500:
            width,height=get_image_dimensions(self.Zdjecie.path)
            if width>height:
                Zapis=temp.crop((width/2-height/2,0,width/2+height/2,height))
            else:
                Zapis=temp.crop((0,height/2-width/2,width,width/2+height/2))
            #Zapis = temp.crop((width/2-250, height/2-250, width/2+250, height/2+250))
           # Zapis=Zapis.resize((500, 500), Image.ANTIALIAS)
            Zapis.save(self.Zdjecie.path)
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


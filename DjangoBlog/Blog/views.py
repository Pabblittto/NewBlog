from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from . import form
from .form import LoginForm
from .form import CustomRegisterForm
# Create your views here.

def registration(request):
    if request.method == 'POST':
        Form = CustomRegisterForm(request.POST)
        if Form.is_valid():
            messages.success(request,'Konto założone')
            user = Form.save()
            profil = models.Profil.objects.create(User=user,Opis='Tymczasowy Opis')
            profil.save()
            user.Profil = profil
            user.save()
            return redirect('home')
        else:
            messages.error(request,"Błąd podczas wypełniania formularza")
            return render(request,'Blog/registration.html',{'form': Form})
    else:
        Form = CustomRegisterForm()
        return render(request,'Blog/registration.html',{'form': Form})

def home(request):
    posts = models.Post.objects.all()
    return render(request,"Blog/home.html",{'posts': posts})

def profile(request):
    if request.user.is_authenticated:
        p = models.Profil.objects.get(User=request.user)
        b = models.Blog.objects.filter(IDAutor = request.user)
    return render(request,"Blog/profile.html",{'account': p, 'blogs':b})

def search(request):
    if (request.method=='GET'):
        if request.GET.get('search')=='':
            messages.error(request,'You need to write what are you looking for')
            return render(request,'Blog/search.html')
        fraza=request.GET.get('search')
        posty=models.Post.objects.filter(Tytul__contains=fraza)
        messages.success(request,f'There are {posty.count()} posts with your phrase')
        return render(request,'Blog/search.html',{'posts':posty,'phase':fraza})
    else:
        messages.error(request,'You need to write what are you looking for')
        return render(request,'Blog/search.html')
        #jeszcze ten search trzeba zmienic zeby patrzył czy szukkamy bloga czy posta

def post(request):
    pass # tu trzeba zrobic pobieranie id z requesta i jazda


def details(request, blog_id):
    b = models.Blog.objects.get(IDBlog = blog_id)
    posts = models.Post.objects.filter(IDBlog = blog_id)
    return render(request,'Blog/blog.html', {'blog': b, 'posts': posts})

        

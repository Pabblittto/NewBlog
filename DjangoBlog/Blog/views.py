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
        typ=request.GET['typ']
        if typ=='Post':
            posty=models.Post.objects.filter(Tytul__contains=fraza)
            messages.success(request,f'There are {posty.count()} posts with your phrase')
            return render(request,'Blog/search.html',{'posts':posty,'phase':fraza,'type':typ})            
        else:
            blogi=models.Blog.objects.filter(Nazwa__contains=fraza)
            messages.success(request,f'There are {blogi.count()} blogs with your phrase')
            return render(request,'Blog/search.html',{'blogs':blogi,'phase':fraza,'type':typ})               
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

def newBlog(request):
    if request.method == 'POST':
        name = request.POST['NewBlogName']
        nowyBlog = models.Blog.objects.create(Nazwa=name,IDAutor=request.user)
        messages.success(request,'Dodano Blog')
        return redirect('profile')
def editOpis(request):
    if request.method == 'POST':
        opis = request.POST.get('OpisForm',False)
        request.user.Opis = opis
        profil = models.Profil.objects.get(User=request.user)
        profil.Opis = opis
        profil.save()
        messages.success(request,'Opis zmieniono')
        return redirect('profile')

def newPost(request):
    if request.method == 'POST':
        tytul = request.POST.get('NewPostTitle',False)
        tresc = request.POST.get('NewPostContent',False)
        if request.POST.get('NewPostPassword',False) != '':
            haslo = request.POST.get('NewPostPassword',False)
            nowyPost = models.Post.objects.create(Tytul=tytul,Tresc=tresc,Haslo=haslo)
        nowyPost = models.Post.objects.create(Tytul=tytul,Tresc=tresc)
        messages.success(request,'Dodano Post')
        return redirect('details')
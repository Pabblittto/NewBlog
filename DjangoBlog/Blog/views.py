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
        

def post(request,post_id):
    post= models.Post.objects.get(IDPost=post_id)
    if post.Haslo:
        if request.session['verification'] == 'verified':
            return render(request,'Blog/post.html',{'post':post})
        else:
            return redirect('home')
    else:
        return render(request,'Blog/post.html')



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

def newPost(request,blog_id):
    if request.method == 'POST':
        tytul = request.POST.get('NewPostTitle',False)
        tresc = request.POST.get('NewPostContent',False)
        b = models.Blog.objects.get(IDBlog = blog_id)
        if request.POST.get('NewPostPassword',False) != '':
            haslo = request.POST.get('NewPostPassword',False)
            nowyPost = models.Post.objects.create(IDBlog=b,Tytul=tytul,Tresc=tresc,Haslo=haslo)
        else :
            nowyPost = models.Post.objects.create(IDBlog=b,Tytul=tytul,Tresc=tresc)
        messages.success(request,'Dodano Post')
        return redirect('/profile/'+str(blog_id)+'/details')
def Password(request,post_id):
    if request.method == 'POST':
        haslo = request.POST.get('PasswordCheck',False)
        post = models.Post.objects.get(IDPost=post_id)
        request.session['verification'] = 'NOTverified'
        if post.Haslo == haslo:
            request.session['verification'] = 'verified'
            return redirect('/post/'+str(post_id)+'/')
        else:          
            messages.error(request,'Podano błędne hasło')
            return redirect('home')
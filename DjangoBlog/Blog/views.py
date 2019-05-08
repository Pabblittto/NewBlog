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
    posts = models.Post.objects.all().order_by('-Data')
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
        typ=request.GET.get('typ',False)
        if typ=='Post':
            posty=models.Post.objects.filter(Tytul__contains=fraza).order_by('-Data')
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
    post = models.Post.objects.get(IDPost=post_id)
    if request.method == 'POST':
        haslo = request.POST.get('PasswordCheck',False)
        if post.Haslo == haslo:
            return render(request,'Blog/post.html',{'post':post})
        else:
            messages.error(request,'Podano błędne hasło')
            return redirect('home')
    else:
        if post.Haslo!='':
            messages.error(request,'Post chroniony hasłem')
            return redirect('home')
        else:
            return render(request,'Blog/post.html',{'post':post})
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
def postDelete(request,blog_id,post_id):
    b = models.Blog.objects.get(IDBlog = blog_id)
    if b.IDAutor == request.user:
        post = models.Post.objects.get(IDPost = post_id).delete()
        posts = models.Post.objects.filter(IDBlog = blog_id)
        messages.error(request,"Usunięto Post")
        return redirect('/profile/'+str(blog_id)+'/details/')
    return redirect('home')

def blogDelete(request,blog_id):
    b = models.Blog.objects.get(IDBlog = blog_id)
    posts = models.Post.objects.filter(IDBlog = blog_id)
    if b.IDAutor == request.user:
        blog = models.Blog.objects.get(IDBlog = blog_id).delete()
        messages.success(request,"Usunięto Blog")
        return redirect('profile')
    else:
        return redirect('home')
def postEdit(request,post_id):
    post = models.Post.objects.get(IDPost = post_id)
    return render(request,'Blog/edit.html', {'post': post})
def postEditTitle(request,post_id):
    post = models.Post.objects.get(IDPost = post_id)
    tytul = request.POST.get('TytulForm')
    post.Tytul = tytul
    post.save()
    return redirect('postEdit',post_id)
def postEditContent(request,post_id):
    post = models.Post.objects.get(IDPost = post_id)
    tresc = request.POST.get('ContentForm')
    post.Tresc = tresc
    post.save()
    return redirect('postEdit',post_id)
def postNewPassword(request,post_id):
    post = models.Post.objects.get(IDPost = post_id)
    pass1 = request.POST.get('NewPasswordForm')
    pass2 = request.POST.get('NewPasswordConfirmForm')
    if pass1 == pass2:
        l = len(pass1)
        if l<=8:
            post.Haslo = pass1
            post.save()
        else:
            messages,error(request,"Haslo jest za dlugie(max 8 znakow)")
    else:
        messages.error(request,"Podano dwa różne hasła")
    return redirect('postEdit',post_id)

def password(request,post_id):
    post = models.Post.objects.get(IDPost = post_id)
    haslo = request.POST.get('OldPasswordForm')
    pass1 = request.POST.get('PasswordForm')
    pass2 = request.POST.get('PasswordConfirmForm')
    if post.Haslo == haslo:
        if pass1 == pass2:
            l = len(pass1)
            if l<=8:
                post.Haslo = pass1
                post.save()
                messages.success(request,"Haslo zmienione")
            else:
                messages.error(request,"Haslo jest za dlugie(max 8 znakow)")
        else:
            messages.error(request,"Podano dwa różne hasła")
    else:
            messages.error(request,"Stare haslo niewlasciwe")
    return redirect('postEdit',post_id)

def passwordDelete(request,post_id):
    post = models.Post.objects.get(IDPost = post_id)
    haslo = post.Haslo
    confirm = request.POST.get('PasswordForm')
    print(confirm)
    print(haslo)
    if haslo == confirm:
        post.Haslo = ''
        post.save()
        messages.success(request,"Haslo usuniete")
    else:
        messages.error(request,"Stare haslo niewlasciwe")
    return redirect('postEdit',post_id)
def newImage(request,post_id):
    post = models.Post.objects.get(IDPost = post_id)
    
    post.save()
    messages.success(request,"To nie działa :D")
    return redirect('postEdit',post_id)
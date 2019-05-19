from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from . import form
from .form import LoginForm
from .form import CustomRegisterForm
from .form import ChangeImageForm, ChangeImageFormPost
from django.contrib.auth.models import User
import os
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from email.parser import HeaderParser
import imaplib
# Create your views here.

def registration(request):
    if request.method == 'POST':
        Form = CustomRegisterForm(request.POST)
        if Form.is_valid():
            messages.success(request,'Wiadomość z potwierdzeniem została wysłana na podany adres Email')  
            user = Form.save()
            user.is_active = False
            profil = models.Profil.objects.create(User=user,Opis='Tymczasowy Opis')
            profil.save()
            user.Profil = profil
            user.save()
            temat = 'Aktywacja konta'
            strona=get_current_site(request)
            tresc = render_to_string('Blog/E-mail.html', {
                'user': user,
                'domena': strona.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            odbiorca = user.email
            email = EmailMessage(
                        temat, tresc, to=[odbiorca]
            )
            email.send()
           # user.is_active = False
            return redirect('home')
        else:
            messages.error(request,"Błąd podczas wypełniania formularza")
            return render(request,'Blog/registration.html',{'form': Form})
    else:
        Form = CustomRegisterForm()
        return render(request,'Blog/registration.html',{'form': Form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        messages.success(request,'Konto zostało aktywowane')  
        return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        #return HttpResponse('Activation link is invalid!')
        messages.success(request,'Potwierdzenie nie powiodło się')  
        return redirect('home')

def home(request):
    posts = models.Post.objects.all().order_by('-Data')
    return render(request,"Blog/home.html",{'posts': posts})

def profile(request):
    if request.user.is_authenticated:
        p = models.Profil.objects.get(User=request.user)
        b = models.Blog.objects.filter(IDAutor = request.user)
        return render(request,"Blog/profile.html",{'account': p, 'blogs':b})
    else:
        messages.error(request,'Nie jesteś zalogowany !')
        return redirect('home')


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
    komentarze = models.Komentarz.objects.filter(IDPost=post_id)
    for k in komentarze:
        print(k.Tresc)
        print(k.Data)
        print(k.IDKomentarz)
        print(k.IDUzytkownik)
        print(k.IDPost)
        print(k.IDPost.Tresc)
    if request.method == 'POST':
        haslo = request.POST.get('PasswordCheck',False)
        if post.Haslo == haslo:
            return render(request,'Blog/post.html',{'post':post,'komentarze': komentarze})
        else:
            messages.error(request,'Podano błędne hasło')
            return redirect('home')
    else:
        if post.Haslo!='':
            messages.error(request,'Post chroniony hasłem')
            return redirect('home')
        else:
            return render(request,'Blog/post.html',{'post':post,'komentarze': komentarze})
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
        # i tu dopiero jest ladowanie zdjecia
            NazwaObrazka= nowyPost.Obraz.url
        ObrazZForma=ChangeImageFormPost(request.POST,request.FILES,instance=nowyPost)
        if ObrazZForma.is_valid():
            if 'Obraz' not in request.POST: # zdjecie zostało wybrane
                if NazwaObrazka!='/Obrazki/Obrazki/default_pic.jpg':
                    tmp=os.getcwd()# pobranie sciezki do tego folderu
                    NazwaObrazka=NazwaObrazka.replace("/","\\")
                    PlikDoWywalenia=tmp+NazwaObrazka
                    try:
                        os.remove(PlikDoWywalenia)
                    except FileNotFoundError:
                        pass # jak nie ma pliku to nie szkodzi  
            ObrazZForma.save()
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


def newImage(request):
    if request.method == 'POST':
        if 'Zdjecie' in request.POST :
            messages.error(request,"Najpierw wybierz obraz")
            return redirect('profile')
        profil= models.Profil.objects.get(User=request.user)
        nazwaObrazka=profil.Zdjecie.url # to przechowuje nazwe pliku
        Obrazek_z_forma=ChangeImageForm(request.POST,request.FILES, instance=profil)           
        if Obrazek_z_forma.is_valid():
            #usuwanie obrazka z bazy jezeli nie jest obrazkiem domyslnym
            if nazwaObrazka!='/Obrazki/Profilowe/default_pic.jpg':
                tmp= os.getcwd()
                nazwaObrazka= nazwaObrazka.replace("/","\\")
                wywal_plik=tmp+nazwaObrazka
                try:
                    os.remove(wywal_plik)
                except FileNotFoundError:
                    pass # jakk nie ma pliku to w sumie nic sie nie dzieje bo i tak go niie chcemy
            Obrazek_z_forma.save()
            messages.success(request,"Obrazek zaktualizowano")
            return redirect('profile')
    else:#ktoś wbił tu z palca
        return redirect('profile') 


def default_pic(request):
    if request.user.is_authenticated:# jezeli jest zalogowany
        profil= models.Profil.objects.get(User=request.user)
        NazwaObrazkaZBazy=profil.Zdjecie.url
        if NazwaObrazkaZBazy=='/Obrazki/Profilowe/default_pic.jpg':# obrazej juz jest defaultowy!
            messages.error(request,'Obrazek juz jest ustawiony na domyślny')
            return redirect('profile')
        else:    
            tmp= os.getcwd()
            NazwaObrazkaZBazy= NazwaObrazkaZBazy.replace("/","\\")
            wywal_plik=tmp+NazwaObrazkaZBazy
            try:
                os.remove(wywal_plik)
            except FileNotFoundError:
                pass # jakk nie ma pliku to w sumie nic sie nie dzieje bo i tak go niie chcemy
            profil.Zdjecie='Profilowe/default_pic.jpg'
            profil.save()
            messages.success(request,'Usunieto obrazek z bazy')
            return redirect('profile')
    else:
        messages.error(request,'Nie jesteś zalogowany!')
        return  redirect('home')


def newComent(request,post_id):
    if request.user.is_authenticated:
        post = models.Post.objects.get(IDPost = post_id)
        tresc = request.POST.get('NewComent')
        new = models.Komentarz.objects.create(IDUzytkownik=request.user,IDPost = post,Tresc=tresc)
    return redirect('post',post_id)

def blog(request,blog_id):
    posts= models.Post.objects.filter(IDBlog=blog_id)# wczytywanie plstow z bloga
    blog= models.Blog.objects.get(IDBlog=blog_id)
    user=blog.IDAutor
    profil= models.Profil.objects.get(User=user)
    return render(request,'Blog/blogPosts.html',{'profil':profil,'posts':posts,'blog':blog,'user':user})

def PostnewImage(request,post_id):
    if request.method == 'POST':
        if 'Obraz' in request.POST :
            messages.error(request,"Najpierw wybierz obraz")
            return redirect('postEdit',post_id)
        Postobj= models.Post.objects.get(IDPost=post_id)
        nazwaObrazka=Postobj.Obraz.url # to przechowuje nazwe pliku
        Obrazek_z_forma=ChangeImageFormPost(request.POST,request.FILES, instance=Postobj)           
        if Obrazek_z_forma.is_valid():
            #usuwanie obrazka z bazy jezeli nie jest obrazkiem domyslnym
            if nazwaObrazka!='/Obrazki/Obrazki/default_pic.jpg':
                tmp= os.getcwd()
                nazwaObrazka= nazwaObrazka.replace("/","\\")
                wywal_plik=tmp+nazwaObrazka
                try:
                    os.remove(wywal_plik)
                except FileNotFoundError:
                    pass # jakk nie ma pliku to w sumie nic sie nie dzieje bo i tak go niie chcemy
            Obrazek_z_forma.save()
            messages.success(request,"Obrazek zaktualizowano")
            return redirect('postEdit',post_id)
    else:#ktoś wbił tu z palca
        return redirect('postEdit',post_id)
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/',views.registration,name='registration'),
    path('',views.home,name='home'),
    path('login/',auth_views.LoginView.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile/',views.profile,name='profile'),
    path('search/',views.search,name='search'),
    path('profile/<int:blog_id>/details/', views.details, name='details'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('profile/<int:blog_id>/newPost/',views.newPost,name='newPost'),
    path('newBlog/',views.newBlog,name='newBlog'),
    path('editOpis/',views.editOpis,name='editOpis'),
    path('newPost/',views.newPost,name='newPost'),
    path('delete/<int:blog_id>/<int:post_id>/',views.postDelete,name='postDelete'),
    path('blog/<int:blog_id>/delete/',views.blogDelete,name='blogDelete'),
    path('post/<int:post_id>/edit/',views.postEdit,name='postEdit'),
    path('post/<int:post_id>/edit/title/',views.postEditTitle,name='postEditTitle'),
    path('post/<int:post_id>/edit/content/',views.postEditContent,name='postEditContent'),
    path('post/<int:post_id>/edit/newPassword/',views.postNewPassword,name='postNewPassword'),
    path('post/<int:post_id>/edit/password/',views.password,name='password'),
    path('post/<int:post_id>/edit/deletePassword/',views.passwordDelete,name='passwordDelete'),
    path('post/<int:post_id>/edit/newImage/',views.PostnewImage,name='newImage'), # to moze trzeba zmenic troche
    path('newImage/',views.newImage,name='newImage'),
    path('blog/<int:blog_id>',views.blog,name='blog'),
    path('default_pic/',views.default_pic,name='default_pic'),
    path('post/<int:post_id>/newComent/',views.newComent,name='newComent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='aktywuj')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
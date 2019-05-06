from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/',views.registration,name='registration'),
    path('',views.home,name='home'),
    path('login/',auth_views.LoginView.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile/',views.profile,name='profile'),
    path('search/',views.search,name='search'),
    path('profile/<int:blog_id>/details', views.details, name='details'),
    path('post/<int:post_id>', views.post, name='post'),
    path('newBlog/',views.newBlog,name='newBlog'),
    path('editOpis/',views.editOpis,name='editOpis'),
    path('newPost/',views.newPost,name='newPost')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from about import searchengine
from django.contrib.auth import views as auth_views
from usertests.views import fehlertest


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mail/', include('emails.urls')),
    path('', include('units.urls')),
    path('tests/', include('usertests.urls')),
    path('community/', include('blog.urls')),
    path('statistics/', include('userstatistics.urls')),
    path('about/', include('about.urls')),
    path('register/', users_views.register, name='register'),
    path('profile/', users_views.profile, name='profile'),
    path('login/', users_views.login_view, name='login'), # alte Methode: auth_views.LoginView.as_view(template_name='users/login.html')
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('start/', users_views.start, name='users-start'),
    # path('start/units', users_views.user_info, name='users-start-units'),
    path('lernweg/', users_views.lernweg, name='users-lernweg'),
    path('lernweg/method/karteikarten', users_views.method_karteikarten, name='method-karteikarten'),
    path('lernweg/method/schriftlich', users_views.method_schriftlich, name='method-schriftlich'),
    path('search/', searchengine.search, name='search'),
    path('account/<int:pk>/delete/', users_views.AccountDeleteView.as_view(), name='account-delete'),
    path('cancel/unit/', users_views.cancel_unit, name='cancel-unit'),
    #path('fehlertest/', fehlertest),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

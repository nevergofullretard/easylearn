from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    post_create,
    update_post,
    post_detail
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),    #mit dem html-tags kann man auf Variablen zugreifen
    path('post/<int:pk>/', post_detail, name='post-detail'),    #<pk> heist primäry key = Primärschlüssel des Posts
    path('post/new/', post_create, name='post-create'),
    path('post/<int:pk>/update/', update_post, name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),

]

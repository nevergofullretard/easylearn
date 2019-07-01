from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback, name='feedback-start'),
    path('newsletter/<int:pk>/unsubscribe', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('newsletter/subscribe', views.newsletter_subscribe, name='newsletter-subscribe'),
    path('send-confirm-mail/', views.send_confirmation, name='confirm-start'),
    path('confirm/<int:pk>/<random_confirm>', views.confirm_email, name='confirm-email'),
    path('forgot-my-password/', views.password_forgot, name='password-forgot'),
    path('password-reset/<int:pk>/<random_confirm>/', views.password_reset, name='password-reset'),
    path('new-password/', views.new_password, name='new-password')
]
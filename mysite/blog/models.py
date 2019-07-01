from datetime import date

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse





class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    linked = models.ManyToManyField(User, blank=True, related_name='linked')
    viewed = models.TextField(null=True) #feststellen, ob markierte User den Post schon angeschaut haben, ob er ihnen als Nachricht angezeigt werden soll oder nicht mehr
    def __str__(self):
        return self.title

    def get_absolute_url(self, ):
        return reverse('post-detail', kwargs={'pk': self.pk})


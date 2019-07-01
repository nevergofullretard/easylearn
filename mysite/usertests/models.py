from django.db import models
from django.contrib.auth.models import User
from units.models import Unit_name



class Unit_pruefung(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit_name, on_delete=models.CASCADE)
    first_voc = models.IntegerField(default=0)
    last_voc = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} {self.unit}'

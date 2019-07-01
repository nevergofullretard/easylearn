from django.db import models
from django.contrib.auth.models import User

class Confirm_email (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10000000000000000000000)

    def __str__(self):
        return f'{self.user}'


class Password_reset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10000000000000000000000)

    def __str(self):
        return f'{self.user}'
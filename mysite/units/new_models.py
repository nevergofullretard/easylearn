from django.db import models
from django.contrib.auth.models import User

class Unit_sprache(models.Model):

    sprache_lang = models.CharField(max_length=20, default='Englisch')
    sprache_kurz = models.CharField(max_length=3, default='EN')

    def __str__(self):
        return self.sprache

class Unit_name(models.Model):
    u_name = models.CharField(max_length=20)  # durch unique=True könnte man Redundanzen verhindern
    sprache = models.ForeignKey(Unit_sprache, on_delete=models.CASCADE, null=True)
    schule = models.ForeignKey(Unit_schule, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.u_name}-{self.schule}-{self.sprache}'

class Anfrage_sprache(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sprache = models.CharField(max_length=20)
    sprache_kurz = models.CharField(max_length=3, default='EN')

    def __str__(self):
        return f'{self.user} Anfrage {self.sprache}'

class Anfrage_schule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schule = models.CharField(max_length=100)



    def __str__(self):
        return f'{self.user} Anfrage {self.schule}'

class Anfrage_unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sprache = models.ForeignKey(Unit_sprache, on_delete=models.CASCADE)
    schule = models.ForeignKey(Unit_schule, on_delete=models.CASCADE)
    unit = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user} Anfrage {self.sprache} {self.schule} {self.unit}'


class Anfrage_words_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit_name, on_delete=models.CASCADE)
    words = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.user} Anfrage {self.unit} words'
#
# class Anfrage_words(models.Model):
#     anfrage = models.ForeignKey(Anfrage_words_user, on_delete=models.CASCADE)
#     words = models.CharField




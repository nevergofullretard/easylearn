from datetime import date


from django.db import models
from django.contrib.auth.models import User

class People(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

    def __str__(self):
        return self.name

class Unit_words(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, default=date.today, null=True)
    unit_name = models.ForeignKey('Unit_name', on_delete=models.CASCADE,)
    italienisch = models.CharField(max_length=200)
    deutsch = models.CharField(max_length=200)
    sidenote = models.CharField(max_length=1000, blank=True)




    '''ACHTUNG!!!  ---> return type "italienisch" nicht ändern, beim Prüfung ist nicht alles dynamisch, kann sich dann verstellen'''
    def __str__(self):
        return self.italienisch # NICHT ÄNDERN!!!


class Unit_schule(models.Model):
    schule = models.CharField(max_length=50)

    def __str__(self):
        return self.schule

# class Sprachen(models.Model):
#     sprache_lang = models.CharField(max_length=20)
#     sprache_kurz = models.CharField(max_length=3)
#
#     def __str__(self):
#         return f'{self.sprache_kurz} - {self.sprache_lang}'



class Unit_sprache(models.Model):
    sprache_lang = models.CharField(max_length=20, default='Englisch')
    sprache_kurz = models.CharField(max_length=3, default='EN')

    def __str__(self):
        return self.sprache_kurz

class Unit_name(models.Model):
    u_name = models.CharField(max_length=100)  # durch unique=True könnte man Redundanzen verhindern
    sprache = models.ForeignKey(Unit_sprache, on_delete=models.CASCADE, null=True)
    schule = models.ForeignKey(Unit_schule, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.u_name}-{self.schule}-{self.sprache}'

class Anfrage_sprache(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sprache_lang = models.CharField(max_length=20, default='Englisch')
    sprache_kurz = models.CharField(max_length=3, default='EN')
    date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)

    def __str__(self):
        return f'{self.user} Anfrage {self.sprache_lang}'

class Anfrage_schule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schule = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)


    def __str__(self):
        return f'{self.user} Anfrage {self.schule}'

class Anfrage_unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sprache = models.ForeignKey(Unit_sprache, on_delete=models.CASCADE)
    schule = models.ForeignKey(Unit_schule, on_delete=models.CASCADE)
    unit = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)

    def __str__(self):
        return f'{self.user} Anfrage {self.sprache} {self.schule} {self.unit}'


class Anfrage_words_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit_name, on_delete=models.CASCADE)
    word_fremdsprache = models.CharField(max_length=1000)
    word_deutsch = models.CharField(max_length=10000, default='')
    sidenote = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.user} Anfrage {self.unit} {self.word_fremdsprache}'





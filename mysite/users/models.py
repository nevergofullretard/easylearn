from django.db import models
from django.contrib.auth.models import User
from units.models import Unit_words, Unit_name
from datetime import date
from PIL import Image


class Units_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # null=True verstehe ich selber noch nicht ganz
    unit = models.ForeignKey(Unit_name, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)

    def __str__(self):
        return f'{self.unit}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voc_bits = models.IntegerField(default=8)   # so viele Vokabeln zeigt es dem User in einem Lerndurchgang an
    first_voc = models.IntegerField(default=0)  # erstes Vokabel des Lerndurchgangs
    current_unit = models.IntegerField(default=0)   # das ist nicht gut, aber es zu ändern würde zu lange dauern (Änderungen in statistic.views und users.views.lernweg!
    last_voc = models.IntegerField(default=0)   # letztes Vokabel des Lerndurchgangs
    pruefung_voc = models.IntegerField(default=4)   # so viele Vokabeln zeigt es dem User bei der Prüfung an
    karteikarten_voc = models.IntegerField(default=4)
    pruefung_umgekehrt = models.BooleanField(default=False) # wenn True, kann es dem User auch Vokabeln von Deutsch auf Italienisch vorschlagen
    units_gemacht = models.ManyToManyField(Units_user, blank=True) # blank=True bedeutet, dass es nicht required ist
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    newsletter = models.BooleanField(default=True)
    toleranz = models.IntegerField(default=51)
    group_number = models.IntegerField(default=1)
    current_unit2 = models.ForeignKey(Unit_name, null=True, on_delete=models.SET_NULL)

    ''' this CharField will be like a CSV-File (comma seperated) and will store the id's
    of The Unit_words in the random generated order, max_length is required, so i hope it will never
    come to problems with the billion or sth, IMPORTANT: never save a vocab with "," because that is used to split the list
    Further information: app: usertests/views/unittest_schriftlich or karteikarten
     '''
    testfield = models.TextField(null=True) #statt CharField TextField nehmen, braucht man kein max_length
    # unittest_karteikarten = models.CharField(null=True, max_length=10000000000000)
    # test_schriftlich = models.CharField(null=True, max_length=10000000000)
    # test_karteikarten = models.CharField(null=True, max_length=100000000)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)


        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Pruefung_voc(models.Model):
    voc = models.IntegerField()

    def __str__(self):
        return f'{self.voc}'

class Words_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # null=True verstehe ich selber noch nicht ganz
    word = models.ForeignKey(Unit_words, on_delete=models.CASCADE)
    right = models.BooleanField(default=True) # if the word is right or wrong, wenn das word richtig ist, dann true
    fuer_pruefung = models.BooleanField(default=False) # wird gebraucht, dass ich weiß ob es für die Prüfung gebraucht wird oder nicht mehr
    lernweg_voc = models.BooleanField(default=True) # ob es noch zum Lernweg gehört oder noch geprüft wird
    date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
    pruefung_reihung = models.IntegerField(default=0)
    fehlertest = models.BooleanField(default=False)
    group = models.IntegerField(default=1)
    eingabe = models.CharField(blank=True, max_length=500)

    def __str__(self):
        return f'{self.word.italienisch}'


#
# class UserInfo(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     date = models.CharField(max_length=50, default='hello')
#
#     def __str__(self):
#         return self.name


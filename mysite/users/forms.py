from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.validators import MinValueValidator, MaxValueValidator
from units.models import Unit_name
from django.contrib.auth import authenticate, login, get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, label='Username oder E-Mail')
    password = forms.CharField(widget=forms.PasswordInput())




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username']


# class UserProfileForm(forms.ModelForm):
#
#     voc_bits = forms.IntegerField(
#         validators=[MinValueValidator(5), MaxValueValidator(12)
#         ])
#
#     class Meta:
#         model = Profile
#         fields = ['voc_bits', 'pruefung_umgekehrt']


class PruefungForm(forms.ModelForm):    # eigene Form für Prüfung, weil nicht mehr Wörter zur Prüfung kommen können als gelernt werden
    voc_bits = forms.IntegerField(label='Größe der Worthäppchen, die du von der Unit lernst (4-12)', max_value=12, min_value=4)
    pruefung_voc = forms.IntegerField(label='Größe der Worthäppchen, die du geprüft wirst (1-12)', max_value=12, min_value=1)
    karteikarten_voc = forms.IntegerField( label='Auswahl, die du bei der Karteikarten-Methode hast (3-12)', max_value=12, min_value=3)
    pruefung_umgekehrt = forms.BooleanField(label='auch Wörter von Fremdsprache auf Deutsch prüfen', required=False)


    class Meta:
        model = Profile
        fields = ['voc_bits', 'pruefung_voc',  'karteikarten_voc', 'pruefung_umgekehrt']

class ImageForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

class ToleranzForm(forms.ModelForm):
    toleranz = forms.IntegerField(label='Toleranz bei der Suche (z.B: 50%)', min_value=1, max_value=100)

    class Meta:
        model = Profile
        fields = ['toleranz']

# class CurrentUnitForm(forms.ModelForm):
#     unit_list = []
#     zahl = 1
#     for i in range(len(Unit_name.objects.all())):
#         unit_list.append((zahl, str(zahl) + '. Unit'))
#         zahl += 1
#
#     current_unit = forms.ChoiceField(choices=unit_list)
#
#     # current_unit = forms.ModelMultipleChoiceField(Unit_name.objects.all())
#     # current_unit = forms.IntegerField()
#
#     class Meta:
#         model = Profile
#         fields = ['current_unit']


class SchriftlichPruefungItForm(forms.Form):
    italienisch = forms.CharField(max_length=300)

class SchriftlichePruefungDeuForm(forms.Form):
    deutsch = forms.CharField(max_length=300)


from django import forms
from . import models
from units.models import Unit_sprache

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))

class UserNewWordsForm(forms.ModelForm):
    alle_sprachen = []
    for sprache in Unit_sprache.objects.all():
        alle_sprachen.append((sprache.id, sprache.sprache_lang))

    sprache = forms.ChoiceField(choices=alle_sprachen)
    class Meta:
        model = models.Anfrage_unit
        fields = ['unit', 'schule']

class UserExistingUnitForm(forms.ModelForm):
    # existing_unit = forms.ModelMultipleChoiceField(queryset=models.Unit_name.objects.all())

    class Meta:
        model = models.Anfrage_words_user
        fields = ['unit']

class NewSchoolForm(forms.ModelForm):
    class Meta:
        model = models.Anfrage_schule
        fields = ['schule']

class NewLangForm(forms.ModelForm):
    # sprache = forms.CharField(max_length=50)

    class Meta:
        model = models.Anfrage_sprache
        fields = ['sprache_lang', 'sprache_kurz']
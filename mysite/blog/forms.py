from django import forms
from .models import Post
from users.models import Images

class PostCreate(forms.ModelForm):
    # content = forms.CharField(initial='Hello')
    class Meta:
        model = Post
        fields = ['content']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['name', 'image']


class LinkImageForm(forms.Form):
    images = []
    for image in Images.objects.all():
        images.append((image.image.url, image.name))

    bild = forms.ChoiceField(choices=images)

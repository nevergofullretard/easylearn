from django import forms
from .models import Post

class PostCreate(forms.ModelForm):
    # content = forms.CharField(initial='Hello')
    class Meta:
        model = Post
        fields = ['content']



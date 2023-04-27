from django import forms
from .models import Spot, Comment


class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = ('title', 'content', 'image', 'category')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'image')
        widgets = {'content': forms.TextInput}

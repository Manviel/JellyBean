from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Board, Photo, Post, Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What?'}
        ),
        max_length=4000
    )

    class Meta:
        model = Topic
        fields = ('subject', 'message')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('message', )


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('name', 'description', )


class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3)
        ]
    )


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )

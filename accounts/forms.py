from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Subject, User, Reader


class SignUpForm(UserCreationForm):
    email = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.EmailInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserInformationUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class ReaderSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_reader = True
        user.save()
        reader = Reader.objects.create(user=user)
        reader.interests.add(*self.cleaned_data.get('interests'))
        return user


class BloggerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_blogger = True
        if commit:
            user.save()
        return user

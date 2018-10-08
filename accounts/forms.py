from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Blogger, Choice, Reader, Subject, User


class UserInformationUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )


class ReaderSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Choice.objects.all(),
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
    birth = forms.DateTimeField(
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={'class': 'datepicker'}
        ),
        input_formats=('%m/%d/%Y', ),
        help_text='MM/DD/YYYY',
        required=True
    )
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_blogger = True
        user.save()
        blogger = Blogger.objects.create(user=user)
        blogger.hobbies.add(*self.cleaned_data.get('hobbies'))
        return user

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Subject, User, Reader, Blogger


class UserInformationUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )


class ReaderSignUpForm(UserCreationForm):
    CHOICES = (
        (1, 'Games'),
        (2, 'Music'),
        (3, 'Sport')
    )
    interests = forms.MultipleChoiceField(
        choices=CHOICES,
        required=False
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

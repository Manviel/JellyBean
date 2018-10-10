from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from social_django.models import UserSocialAuth

from .forms import (BloggerSignUpForm, ReaderSignUpForm,
                    UserInformationUpdateForm)
from .models import User
from .tasks import email_greet


def choose(request):
    return render(request, 'includes/choose.html')


class ReaderSignUpView(CreateView):
    model = User
    form_class = ReaderSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'reader'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(
            self.request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        email_greet(user.email)
        return redirect('home')


class BloggerSignUpView(CreateView):
    model = User
    form_class = BloggerSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'blogger'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(
            self.request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return redirect('home')


@login_required
def updateView(request):
    if request.method == 'POST':
        form = UserInformationUpdateForm(
            data=request.POST,
            instance=request.user
        )
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Has been update')
    else:
        form = UserInformationUpdateForm(instance=request.user)
    return render(request, 'my_account.html', {'form': form})


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = (user.social_auth.count() >
                      1 or user.has_usable_password())

    return render(request, 'settings.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect
    })


@method_decorator(login_required, name='dispatch')
class InterestsView(UpdateView):
    form_class = ReaderSignUpForm
    template_name = 'my_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.reader

    def form_valid(self, form):
        return super().form_valid(form)

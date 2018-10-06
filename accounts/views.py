from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView

from .forms import SignUpForm, UserInformationUpdateForm, BloggerSignUpForm, ReaderSignUpForm
from .models import User, Reader


def choose(request):
    return render(request, 'includes/choose.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class ReaderSignUpView(CreateView):
    model = User
    form_class = ReaderSignUpForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'reader'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
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
        login(self.request, user)
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    form_class = UserInformationUpdateForm
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class interestsView(UpdateView):
    model = Reader
    form_class = ReaderSignUpForm
    template_name = 'interests.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.reader

    def form_valid(self, form):
        return super().form_valid(form)

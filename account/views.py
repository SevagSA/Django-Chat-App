from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from .models import User
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from .utils import redirect_to_nxt


class RegisterUserView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def get_success_url(self):
        messages.success(self.request, 'Account registered. Please login.')
        return reverse('account:login')


def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect_to_nxt(request, 'chat:home')
            else:
                messages.error(request, 'Invalid login')
                form = UserLoginForm(request.POST)
        else:
            messages.error(request, 'Invalid login')
            form = UserLoginForm(request.POST)
    return render(request, 'account/login.html', {'form': form})


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'account/update_account.html'

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def get_success_url(self):
        messages.success(self.request, 'Account udpated')
        return reverse('account:profile', kwargs={'email': self.get_object().email})


def profile_page(request, email):
    user = User.objects.get(email=email)
    return render(request, 'account/profile_page.html', {'profile_user': user})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect_to_nxt(request, 'chat:home')

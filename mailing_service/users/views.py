from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages


class RegisterView(CreateView):
    """Класс для регистрации пользователей"""
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Аккаунт {username} успешно создан!')
        return response


class LoginView(FormView):
    """Класс для авторизации пользователей"""
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')  # Укажите ваш URL

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Класс для выхода пользователя"""
    next_page = reverse_lazy('home')  # Укажите ваш URL

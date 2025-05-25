from django.views.generic import View, CreateView, FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    """Класс для регистрации пользователей"""
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Аккаунт {form.cleaned_data.get("username")} успешно создан!'
        )
        return response


class LoginView(FormView):
    """Класс для авторизации пользователей"""
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f'Добро пожаловать, {user.username}!')
        return super().form_valid(form)


class CustomLogoutView(View):
    """Класс для выхода пользователя"""
    next_page = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.next_page)

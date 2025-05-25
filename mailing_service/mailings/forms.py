from django import forms
from .models import Mailing, Message, Recipient
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема сообщения'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Текст сообщения'
            }),
        }


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@domain.com'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванов Иван Иванович'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Дополнительная информация'
            }),
        }


class MailingForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = Message.objects.filter(owner=user)
        self.fields['recipients'].queryset = Recipient.objects.filter(owner=user)

        # Стилизация полей
        self.fields['start_time'].widget = forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        )
        self.fields['end_time'].widget = forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'}
        )
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
        self.fields['recipients'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'status', 'message', 'recipients']
        labels = {
            'start_time': 'Дата и время начала',
            'end_time': 'Дата и время окончания',
            'status': 'Статус рассылки',
            'message': 'Сообщение',
            'recipients': 'Получатели',
        }
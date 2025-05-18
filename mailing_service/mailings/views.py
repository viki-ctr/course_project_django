from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from .models import Mailing, MailingAttempt, Recipient


class SendMailingView(LoginRequiredMixin, FormView):
    def post(self, request, *args, **kwargs):
        mailing = Mailing.objects.get(id=kwargs['pk'])
        if mailing.owner != request.user:
            return HttpResponseForbidden()

        for recipient in mailing.recipients.all():
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    'noreply@example.com',
                    [recipient.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='success',
                    server_response='OK',
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='failed',
                    server_response=str(e),
                )

        return redirect('mailings:detail', pk=mailing.pk)


class HomeView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context['total_mailings'] = Mailing.objects.filter(owner=user).count()
            context['active_mailings'] = Mailing.objects.filter(
                owner=user,
                status='started'
            ).count()
            context['unique_recipients'] = Recipient.objects.filter(
                owner=user
            ).distinct().count()
        else:
            context['total_mailings'] = 0
            context['active_mailings'] = 0
            context['unique_recipients'] = 0

        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'message', 'recipients']
    template_name = 'mailings/mailing_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
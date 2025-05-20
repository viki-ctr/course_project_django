from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Mailing, Message, Recipient
from .forms import MailingForm, MessageForm, RecipientForm


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'
    permission_required = 'mailings.can_view_all_mailings'
    raise_exception = True
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_view_all_mailings'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset.select_related('message', 'owner').prefetch_related('recipients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_create'] = self.request.user.has_perm('mailings.add_mailing')
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Рассылка успешно создана!')
        return response


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    permission_required = 'mailings.can_edit_any_mailing'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_edit_any_mailing'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('mailings:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Рассылка успешно обновлена!')
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'
    permission_required = 'mailings.can_view_all_mailings'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_view_all_mailings'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset.select_related('message', 'owner').prefetch_related('recipients', 'attempts')


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:list')
    permission_required = 'mailings.can_edit_any_mailing'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_edit_any_mailing'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Рассылка успешно удалена!')
        return super().delete(request, *args, **kwargs)


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'
    permission_required = 'mailings.can_view_all_messages'
    raise_exception = True
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_view_all_messages'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset.select_related('owner')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Сообщение успешно создано!')
        return response


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    permission_required = 'mailings.can_edit_any_message'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_edit_any_message'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('mailings:message_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Сообщение успешно обновлено!')
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    context_object_name = 'message'
    permission_required = 'mailings.can_view_all_messages'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_view_all_messages'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset.select_related('owner')


class RecipientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Recipient
    template_name = 'mailings/recipient_list.html'
    context_object_name = 'recipients'
    permission_required = 'mailings.can_view_all_recipients'
    raise_exception = True
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_view_all_recipients'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailings/recipient_form.html'
    success_url = reverse_lazy('mailings:recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Получатель успешно добавлен!')
        return response


class RecipientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailings/recipient_form.html'
    permission_required = 'mailings.can_edit_any_recipient'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_edit_any_recipient'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('mailings:recipient_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Данные получателя успешно обновлены!')
        return super().form_valid(form)


class RecipientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Recipient
    template_name = 'mailings/recipient_detail.html'
    context_object_name = 'recipient'
    permission_required = 'mailings.can_view_all_recipients'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_view_all_recipients'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class RecipientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'mailings/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailings:recipient_list')
    permission_required = 'mailings.can_edit_any_recipient'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('mailings.can_edit_any_recipient'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Получатель успешно удален!')
        return super().delete(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='started').count()
        context['unique_recipients'] = Recipient.objects.distinct().count()
        return context

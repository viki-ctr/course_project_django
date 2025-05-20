from django.db import models
from django.conf import settings
from django.utils import timezone


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Текст письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        permissions = [
            ('can_view_all_messages', 'Может просматривать все сообщения'),
            ('can_edit_any_message', 'Может редактировать любые сообщения'),
        ]

    def __str__(self):
        return self.subject


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        permissions = [
            ('can_view_all_recipients', 'Может просматривать всех получателей'),
            ('can_edit_any_recipient', 'Может редактировать любых получателей'),
        ]

    def __str__(self):
        return f'{self.full_name} ({self.email})'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name='Сообщение'
    )
    recipients = models.ManyToManyField(
        Recipient,
        verbose_name='Получатели'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('can_view_all_mailings', 'Может просматривать все рассылки'),
            ('can_edit_any_mailing', 'Может редактировать любые рассылки'),
            ('can_disable_mailing', 'Может отключать рассылки'),
        ]

    def __str__(self):
        return f'Рассылка #{self.id} ({self.get_status_display()})'

    def save(self, *args, **kwargs):
        # Автоматическое обновление статуса
        now = timezone.now()
        if self.start_time <= now <= self.end_time:
            self.status = 'started'
        elif now > self.end_time:
            self.status = 'completed'
        super().save(*args, **kwargs)


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время попытки'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Статус'
    )
    server_response = models.TextField(
        blank=True,
        verbose_name='Ответ сервера'
    )

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылок'
        ordering = ['-attempt_time']

    def __str__(self):
        return f'Попытка {self.mailing} - {self.get_status_display()}'

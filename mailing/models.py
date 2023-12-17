from django.db import models

from config import settings

# Create your models here.
NULLABLE = {
    'null': True,
    'blank': True
}


class Client(models.Model):
    email = models.EmailField(verbose_name='Электронная почта')
    FIO = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.CharField(max_length=150, verbose_name='Комментарий')
    #owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.FIO})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    PERIOD_VARIANTS = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_VARIANTS = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('done', 'Завершена')
    ]

    start_time = models.DateField(**NULLABLE, verbose_name='Начало времени рассылки')
    finish_time = models.DateField(**NULLABLE, verbose_name='Конец времени рассылки')
    send_frequency = models.CharField(max_length=20, choices=PERIOD_VARIANTS, **NULLABLE, verbose_name='Периодичность')
    mailing_status = models.CharField(max_length=20, choices=STATUS_VARIANTS, verbose_name='Статус')
    mailing_clients = models.ManyToManyField(Client, verbose_name='Клиент')
    title_message = models.CharField(max_length=150, verbose_name='Тема письма')
    body_message = models.TextField(verbose_name='Тело письма', **NULLABLE)
    last_date = models.DateField(verbose_name='Дата последней рассылки', **NULLABLE)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f"Рассылка {self.subject} в {self.start_time}-{self.finish_time} ({self.send_frequency})"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    permissions = [
        (
            'deactivate_mailing',
            'Can deactivate settings'
        )
    ]


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    log_status = models.CharField(max_length=20, choices=STATUSES, verbose_name='Статус попытки')
    log_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, **NULLABLE, verbose_name='Рассылка')
    response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')

    def __str__(self):
        return f"{self.log_client} - {self.log_mailing} ({self.log_status}) в {self.created_time}"

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'

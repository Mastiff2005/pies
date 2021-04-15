from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    REQUIRED_FIELDS = []

    organization = models.CharField(
        verbose_name='Организация', max_length=50,
        help_text='Укажите название организации - для организаций/'
        'имя - для физических лиц'
        )
    email = models.CharField(max_length=50, verbose_name='Email')
    phone = models.SlugField(
        verbose_name='Телефон', max_length=50,
        help_text='Обязательное поле. Укажите телефон '
                  'в формате 8-XXX-XXX-XX-XX.'
    )
    address = models.CharField(
        verbose_name='Адрес доставки', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.username

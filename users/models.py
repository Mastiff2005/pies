from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    organization = User.first_name
    phone = models.SlugField(
        verbose_name='Телефон', max_length=50,
        help_text='Обязательное поле. Укажите телефон '
                  'в формате 8-XXX-XXX-XX-XX.'
        )
    address = models.CharField(
        verbose_name='Адрес доставки', max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

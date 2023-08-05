from django.core.mail import send_mail
from django.db import models

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from Callboard import settings


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'



class Category(models.Model):
    tank = 'Танк'
    healer = 'Хил'
    damager = 'ДД'
    guild_master = 'Гилдмастер'
    quest_giver = 'Квестгивер'
    smith = 'Кузнец'
    tanner = 'Кожевник'
    potion_maker = 'Зельевар'
    spell_master = 'Мастер заклинаний'

    CATEGORIES = [
        (tank, 'Танк'),
        (healer, 'Хил'),
        (damager, 'ДД'),
        (guild_master, 'Гилдмастер'),
        (quest_giver, 'Квестгивер'),
        (smith, 'Кузнец'),
        (tanner, 'Кожевник'),
        (potion_maker, 'Зельевар'),
        (spell_master, 'Мастер заклинаний'),
    ]

    name = models.CharField(max_length=20, choices=CATEGORIES, default=tank)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    title = models.CharField(max_length=50, default='Заголовок')
    author = models.CharField(max_length=50, default='Автор')
    text = RichTextField('Содержание')
    time_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    text = models.TextField(blank=False, default='Комментарий')
    time_in = models.DateTimeField(auto_now_add=True)

    def date_in(self):
        return self.time_in.date()

    def send_notification_email(self):
        subject = 'Комментарий на ваш пост'
        message = 'Здравствуйте!\n\nНа ваш пост "{}" появился новый комментарий.'.format(self.post.title)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.post.author.email]
        send_mail(subject, message, from_email, recipient_list)

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name} ({self.address})'

    class Meta:
        verbose_name = 'Место встречи'
        verbose_name_plural = 'Место встречи'
        ordering = ['id']


class Participant(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Участники'
        verbose_name_plural = 'Участники'
        ordering = ['id']


class MeetUp(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Participant, blank=True)  # из-за связи с бд каждый учстник принимат участие в каждом сорвеновании
    organizer_email = models.EmailField()

    def __str__(self):
        return f'{self.slug} - {self.title}'

    def get_absolute_url(self):
        return reverse('meetup-detail', kwargs={'meetup_slug': self.slug})

    class Meta:
        verbose_name = 'Встречи'
        verbose_name_plural = 'Встречи'
        ordering = ['id', 'location', 'title']



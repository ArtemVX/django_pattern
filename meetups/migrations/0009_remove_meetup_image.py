# Generated by Django 4.1.3 on 2022-11-28 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetups', '0008_alter_meetup_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetup',
            name='image',
        ),
    ]

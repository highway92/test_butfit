# Generated by Django 3.2.12 on 2022-03-13 08:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lesson', '0002_lesson_credit_earned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='participation',
            field=models.ManyToManyField(db_column='participation', related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]

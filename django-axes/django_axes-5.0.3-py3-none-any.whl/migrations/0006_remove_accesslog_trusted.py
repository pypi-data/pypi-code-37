# Generated by Django 2.0.4 on 2019-03-13 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('axes', '0005_remove_accessattempt_trusted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesslog',
            name='trusted',
        ),
    ]

# Generated by Django 2.1.8 on 2019-05-08 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handytools', '0002_textphrase_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='textphrase',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='textphrase',
            name='language',
            field=models.CharField(choices=[('global', 'Global'), ('en', 'English'), ('fr', 'French')], default='global', max_length=6, verbose_name='Language'),
        ),
    ]

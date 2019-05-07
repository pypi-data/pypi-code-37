# Generated by Django 2.2.1 on 2019-05-07 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextPhrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase_type', models.CharField(db_index=True, max_length=255, verbose_name='Phrase Type')),
                ('text', models.TextField(verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Text Phrase',
                'verbose_name_plural': 'Text Phrases',
                'ordering': ('phrase_type',),
            },
        ),
    ]

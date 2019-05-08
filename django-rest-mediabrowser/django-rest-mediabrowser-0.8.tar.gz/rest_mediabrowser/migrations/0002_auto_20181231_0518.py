# Generated by Django 2.1.4 on 2018-12-31 05:18

import django.core.files.storage
from django.db import migrations, models
import rest_mediabrowser.models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_mediabrowser', '0001_squashed_0004_auto_20181229_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='file',
            field=models.FileField(max_length=500, storage=django.core.files.storage.FileSystemStorage(location='/app/server/mediabrowser_files'), upload_to=rest_mediabrowser.models.file_upload_path, verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='mediaimage',
            name='height',
            field=models.IntegerField(blank=True, null=True, verbose_name='height'),
        ),
        migrations.AlterField(
            model_name='mediaimage',
            name='image',
            field=models.ImageField(height_field='height', max_length=500, storage=django.core.files.storage.FileSystemStorage(location='/app/server/mediabrowser_files'), upload_to=rest_mediabrowser.models.image_upload_path, verbose_name='image', width_field='width'),
        ),
        migrations.AlterField(
            model_name='mediaimage',
            name='width',
            field=models.IntegerField(blank=True, null=True, verbose_name='width'),
        ),
    ]

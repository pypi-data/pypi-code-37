# Generated by Django 2.1.4 on 2019-01-05 11:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rest_mediabrowser', '0002_auto_20181231_0518'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='collectionpermission',
            unique_together={('user', 'collection')},
        ),
        migrations.AlterUniqueTogether(
            name='filepermission',
            unique_together={('user', 'file')},
        ),
        migrations.AlterUniqueTogether(
            name='imagepermission',
            unique_together={('user', 'image')},
        ),
    ]

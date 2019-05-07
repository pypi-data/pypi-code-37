# Generated by Django 2.1.2 on 2018-11-04 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_auto_20181031_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteproperty',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='type',
            field=models.IntegerField(choices=[(1, '店铺'), (2, '文章'), (3, '论坛')], default=1, verbose_name='类别'),
        ),
    ]

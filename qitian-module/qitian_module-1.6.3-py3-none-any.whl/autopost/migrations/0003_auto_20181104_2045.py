# Generated by Django 2.1.2 on 2018-11-04 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopost', '0002_auto_20181023_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='link_add',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='外链地址'),
        ),
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.IntegerField(choices=[(1, '文章'), (2, '外链'), (3, '内链')], default=1, verbose_name='文章类别'),
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.IntegerField(choices=[(2, '主菜单'), (0, '隐藏'), (1, '显示')], default=1, verbose_name='状态'),
        ),
    ]

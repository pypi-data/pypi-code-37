# Generated by Django 2.1.4 on 2019-05-03 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tom_dataproducts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataproduct',
            name='product_id',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]

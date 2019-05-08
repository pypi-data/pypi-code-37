# Generated by Django 2.2 on 2019-04-26 06:52

from django.db import migrations, models

from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
# from django.contrib.postgres.operations import BtreeGinExtension


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        # install btree_gin extension if you are running as 'postgres'
        # BtreeGinExtension(),

        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(db_index=True, max_length=64)),
                ('sender', models.CharField(db_index=True, max_length=64)),
                ('effective_date', models.DateTimeField(db_index=True)),
                ('received_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('marketplace_purchase', JSONField()),
            ],
        ),
        migrations.AddIndex(
            model_name='purchase',
            index=GinIndex(fastupdate=False, fields=['marketplace_purchase'],
                           name='tcms_github_marketplace_gin'),
        ),
    ]

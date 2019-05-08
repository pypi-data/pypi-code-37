# Generated by Django 2.0.1 on 2018-01-16 12:11

from django.db import migrations, models
import django.db.models.deletion
import edc_sites.models


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("edc_appointment", "0013_delete_holiday"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="appointment",
            managers=[("on_site", edc_sites.models.CurrentSiteManager())],
        ),
        migrations.AddField(
            model_name="appointment",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="sites.Site",
            ),
        ),
        migrations.AddField(
            model_name="historicalappointment",
            name="site",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="sites.Site",
            ),
        ),
    ]

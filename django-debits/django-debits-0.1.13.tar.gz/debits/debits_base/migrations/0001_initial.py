# Generated by Django 2.2.1 on 2019-05-07 16:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_qty', models.IntegerField(default=1)),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_time', models.DateTimeField(auto_now_add=True, verbose_name='Payment time')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='debits_base.BaseTransaction')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentProcessor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='The name of the company')),
                ('url', models.URLField(max_length=255)),
                ('klass_app_label', models.CharField(max_length=100, verbose_name='Django app with the model')),
                ('klass_model', models.CharField(max_length=100, verbose_name='Python model class name')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Product name')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('blocked', models.BooleanField(default=False)),
                ('gratis', models.BooleanField(default=False)),
                ('shipping', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('reminders_sent', models.SmallIntegerField(db_index=True, default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='debits_base.Item')),
                ('old_subscription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_subscription', to='debits_base.Purchase')),
                ('payment', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='debits_base.Payment')),
            ],
        ),
        migrations.CreateModel(
            name='SimpleItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.Item')),
            ],
            bases=('debits_base.item',),
        ),
        migrations.CreateModel(
            name='SimplePayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.Payment')),
            ],
            bases=('debits_base.payment',),
        ),
        migrations.CreateModel(
            name='SimplePurchase',
            fields=[
                ('purchase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.Purchase')),
                ('status', models.SmallIntegerField(default=1, verbose_name='Payment status')),
            ],
            bases=('debits_base.purchase',),
        ),
        migrations.CreateModel(
            name='SimpleTransaction',
            fields=[
                ('basetransaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.BaseTransaction')),
            ],
            bases=('debits_base.basetransaction',),
        ),
        migrations.CreateModel(
            name='SubscriptionItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.Item')),
                ('grace_period_unit', models.SmallIntegerField(default=1)),
                ('grace_period_count', models.SmallIntegerField(default=20)),
                ('payment_period_unit', models.SmallIntegerField(default=3)),
                ('payment_period_count', models.SmallIntegerField(default=1)),
                ('trial_period_unit', models.SmallIntegerField(default=3)),
                ('trial_period_count', models.SmallIntegerField(default=0)),
            ],
            bases=('debits_base.item',),
        ),
        migrations.CreateModel(
            name='SubscriptionTransaction',
            fields=[
                ('basetransaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.BaseTransaction')),
            ],
            bases=('debits_base.basetransaction',),
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='debits_base.Product'),
        ),
        migrations.AddField(
            model_name='basetransaction',
            name='processor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='debits_base.PaymentProcessor'),
        ),
        migrations.AddField(
            model_name='basetransaction',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='debits_base.Purchase'),
        ),
        migrations.CreateModel(
            name='AggregateItem',
            fields=[
                ('simpleitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.SimpleItem')),
            ],
            bases=('debits_base.simpleitem',),
        ),
        migrations.CreateModel(
            name='AggregatePurchase',
            fields=[
                ('simplepurchase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.SimplePurchase')),
            ],
            bases=('debits_base.simplepurchase',),
        ),
        migrations.CreateModel(
            name='SubscriptionPurchase',
            fields=[
                ('purchase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.Purchase')),
                ('due_payment_date', models.DateField(db_index=True, default=datetime.date.today)),
                ('payment_deadline', models.DateField(db_index=True, null=True)),
                ('trial', models.BooleanField(db_index=True, default=False)),
                ('subinvoice', models.PositiveIntegerField(default=1)),
                ('subscription_reference', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('processor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='debits_base.PaymentProcessor')),
            ],
            bases=('debits_base.purchase',),
        ),
        migrations.CreateModel(
            name='AutomaticPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.Payment')),
                ('subscription_reference', models.CharField(max_length=255, null=True)),
                ('processor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='debits_base.PaymentProcessor')),
            ],
            bases=('debits_base.payment',),
        ),
        migrations.AddField(
            model_name='purchase',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childs', to='debits_base.AggregatePurchase'),
        ),
        migrations.CreateModel(
            name='ProlongPurchase',
            fields=[
                ('simplepurchase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='debits_base.SimplePurchase')),
                ('period_unit', models.SmallIntegerField(default=3)),
                ('period_count', models.SmallIntegerField(default=0)),
                ('prolonged', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='debits_base.SubscriptionPurchase')),
            ],
            bases=('debits_base.simplepurchase',),
        ),
    ]

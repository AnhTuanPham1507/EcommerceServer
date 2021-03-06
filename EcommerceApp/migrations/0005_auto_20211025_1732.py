# Generated by Django 3.2.8 on 2021-10-25 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcommerceApp', '0004_auto_20211019_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(choices=[('BANED', 'banned'), ('ACTIVE', 'active'), ('PENDING', 'pending')], default='ACTIVE', max_length=7),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipped_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

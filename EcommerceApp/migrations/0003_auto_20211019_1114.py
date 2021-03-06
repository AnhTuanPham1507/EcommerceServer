# Generated by Django 3.2.8 on 2021-10-19 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcommerceApp', '0002_auto_20211014_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'active'), ('PENDING', 'pending'), ('BANED', 'banned')], default='ACTIVE', max_length=7),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipped_date',
            field=models.DateTimeField(blank=True, default='00:00:00'),
        ),
    ]

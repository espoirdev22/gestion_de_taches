# Generated by Django 4.2.19 on 2025-03-13 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='completion_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='performance',
            name='on_time_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]

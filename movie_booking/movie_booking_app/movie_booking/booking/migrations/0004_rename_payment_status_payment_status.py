# Generated by Django 5.1.6 on 2025-02-24 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_movie_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment_status',
            new_name='status',
        ),
    ]

# Generated by Django 4.1.2 on 2022-10-27 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='service',
            unique_together={('title', 'service_type')},
        ),
    ]

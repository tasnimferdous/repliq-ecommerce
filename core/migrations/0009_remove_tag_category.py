# Generated by Django 4.1.3 on 2023-04-20 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='category',
        ),
    ]
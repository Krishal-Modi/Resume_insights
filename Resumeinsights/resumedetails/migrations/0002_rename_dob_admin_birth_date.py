# Generated by Django 5.1.2 on 2024-10-10 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resumedetails', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='dob',
            new_name='birth_date',
        ),
    ]

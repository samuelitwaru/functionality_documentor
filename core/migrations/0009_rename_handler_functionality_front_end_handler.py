# Generated by Django 4.0.3 on 2022-07-31 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_app_folders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='functionality',
            old_name='handler',
            new_name='front_end_handler',
        ),
    ]

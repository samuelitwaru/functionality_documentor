# Generated by Django 4.0.6 on 2022-07-24 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_file_dot_notation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='folders',
            new_name='ignore_files',
        ),
    ]

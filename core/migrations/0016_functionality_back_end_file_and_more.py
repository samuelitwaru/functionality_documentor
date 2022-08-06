# Generated by Django 4.0.3 on 2022-08-05 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_file_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='functionality',
            name='back_end_file',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='functionality',
            name='front_end_file',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-15 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='functionality',
            name='app',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.app'),
            preserve_default=False,
        ),
    ]

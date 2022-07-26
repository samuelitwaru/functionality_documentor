# Generated by Django 4.0.6 on 2022-07-16 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_app_options_app_users_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='users',
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(default='', max_length=512)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.app')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='functionality',
            name='users',
            field=models.ManyToManyField(related_name='functionalities', to='core.appuser'),
        ),
    ]

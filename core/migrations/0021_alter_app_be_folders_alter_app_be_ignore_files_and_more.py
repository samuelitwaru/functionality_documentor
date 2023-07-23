# Generated by Django 4.0.6 on 2023-07-12 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_app_collaborators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='be_folders',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='app',
            name='be_ignore_files',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='app',
            name='be_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='be_repo',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='be_token',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='fe_folders',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='app',
            name='fe_ignore_files',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='app',
            name='fe_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='fe_repo',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='fe_token',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.CreateModel(
            name='FunctionalityCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=128)),
                ('Functionalities', models.ManyToManyField(to='core.functionality')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
# Generated by Django 4.2.3 on 2023-08-03 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_api', '0004_alter_movie_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='download/videos/'),
        ),
    ]

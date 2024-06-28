# Generated by Django 4.2.12 on 2024-06-28 07:02

import django.core.files.storage
from django.db import migrations, models
import user_tasks.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_tasks', '0005_alter_usertaskartifact_id_alter_usertaskstatus_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertaskartifact',
            name='file',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(), upload_to=user_tasks.models.file_path_by_user),
        ),
    ]

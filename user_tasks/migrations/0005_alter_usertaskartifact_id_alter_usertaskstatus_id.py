# Generated by Django 4.2.10 on 2024-04-22 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_tasks', '0004_url_textfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertaskartifact',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usertaskstatus',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
# Generated by Django 5.2 on 2025-05-09 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='data/user_photo/%Y/%m/%d/'),
        ),
    ]

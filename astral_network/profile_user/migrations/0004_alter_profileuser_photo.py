# Generated by Django 5.2 on 2025-05-09 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_user', '0003_alter_profileuser_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photo/%Y/%m/%d/'),
        ),
    ]

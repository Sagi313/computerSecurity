# Generated by Django 3.2.9 on 2021-12-31 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0004_userchatmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userchatmessage',
            old_name='user_id',
            new_name='user',
        ),
    ]

# Generated by Django 3.2.6 on 2021-08-07 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_chatroom_room_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatroom',
            old_name='members',
            new_name='users',
        ),
    ]
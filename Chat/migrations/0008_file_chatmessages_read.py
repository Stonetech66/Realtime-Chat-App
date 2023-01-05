# Generated by Django 4.1.1 on 2023-01-03 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Socket', '0007_alter_conversation_last_chatted'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files')),
            ],
        ),
        migrations.AddField(
            model_name='chatmessages',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]

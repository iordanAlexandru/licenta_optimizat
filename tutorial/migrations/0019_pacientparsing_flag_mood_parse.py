# Generated by Django 3.0.1 on 2020-05-13 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0018_auto_20200509_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacientparsing',
            name='flag_mood_parse',
            field=models.BooleanField(default=False),
        ),
    ]

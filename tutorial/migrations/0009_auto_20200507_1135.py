# Generated by Django 3.0.1 on 2020-05-07 08:35

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0008_auto_20200507_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacientparsing',
            name='negative_problems',
            field=jsonfield.fields.JSONField(default=[]),
        ),
    ]

# Generated by Django 3.0.1 on 2020-05-14 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0020_remove_pacientparsing_flag_mood_parse'),
    ]

    operations = [
        migrations.AddField(
            model_name='alzheimerparsing',
            name='tutore',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutorial.Tutore'),
        ),
        migrations.AddField(
            model_name='depressionparsing',
            name='tutore',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutorial.Tutore'),
        ),
        migrations.AddField(
            model_name='diabetesparsing',
            name='tutore',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutorial.Tutore'),
        ),
    ]
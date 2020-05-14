# Generated by Django 3.0.1 on 2020-05-09 09:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0017_auto_20200509_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pacientparsing',
            name='mood_rating_list',
        ),
        migrations.CreateModel(
            name='DiabetesParsing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_rating', models.CharField(default=0, max_length=100, validators=[django.core.validators.int_list_validator])),
                ('pacientparse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.PacientParsing')),
            ],
        ),
        migrations.CreateModel(
            name='DepressionParsing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_rating', models.CharField(default=0, max_length=100, validators=[django.core.validators.int_list_validator])),
                ('pacientparse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.PacientParsing')),
            ],
        ),
        migrations.CreateModel(
            name='AlzheimerParsing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_rating', models.CharField(default=0, max_length=100, validators=[django.core.validators.int_list_validator])),
                ('pacientparse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.PacientParsing')),
            ],
        ),
    ]
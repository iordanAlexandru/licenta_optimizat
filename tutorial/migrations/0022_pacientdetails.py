# Generated by Django 3.0.1 on 2020-05-22 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0021_auto_20200514_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='PacientDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_book', models.CharField(blank=True, max_length=200)),
                ('fav_movie', models.CharField(blank=True, max_length=200)),
                ('fav_song', models.CharField(blank=True, max_length=200)),
                ('fav_activity', models.CharField(blank=True, max_length=200)),
                ('fav_passion', models.CharField(blank=True, max_length=200)),
                ('fav_game', models.CharField(blank=True, max_length=200)),
                ('hangout', models.IntegerField(blank=True)),
                ('pacient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.Pacient')),
            ],
        ),
    ]

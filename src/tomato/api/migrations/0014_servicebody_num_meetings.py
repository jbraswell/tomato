# Generated by Django 2.2.4 on 2019-12-01 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20191201_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicebody',
            name='num_meetings',
            field=models.IntegerField(default=0),
        ),
    ]

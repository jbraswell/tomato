# Generated by Django 2.0.2 on 2018-03-09 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180307_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetinginfo',
            name='contact_email_1',
        ),
        migrations.RemoveField(
            model_name='meetinginfo',
            name='contact_email_2',
        ),
        migrations.RemoveField(
            model_name='meetinginfo',
            name='contact_name_1',
        ),
        migrations.RemoveField(
            model_name='meetinginfo',
            name='contact_name_2',
        ),
        migrations.RemoveField(
            model_name='meetinginfo',
            name='contact_phone_1',
        ),
        migrations.RemoveField(
            model_name='meetinginfo',
            name='contact_phone_2',
        ),
    ]
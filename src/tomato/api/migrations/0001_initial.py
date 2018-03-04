# Generated by Django 2.0.2 on 2018-03-04 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('source_id', models.BigIntegerField()),
                ('key_string', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('language', models.CharField(default='en', max_length=7)),
                ('world_id', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImportProblem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('source_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('weekday', models.SmallIntegerField(choices=[(1, 'Sunday'), (2, 'Monday'), (3, 'Tuesday'), (4, 'Wednesday'), (5, 'Thursday'), (6, 'Friday'), (7, 'Saturday')])),
                ('start_time', models.TimeField(null=True)),
                ('duration', models.TimeField(null=True)),
                ('language', models.CharField(max_length=7, null=True)),
                ('latitude', models.DecimalField(decimal_places=12, max_digits=15)),
                ('longitude', models.DecimalField(decimal_places=12, max_digits=15)),
                ('published', models.BooleanField(default=False)),
                ('formats', models.ManyToManyField(to='api.Format')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingInfo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('contact_name_1', models.CharField(max_length=255, null=True)),
                ('contact_email_1', models.EmailField(max_length=254, null=True)),
                ('contact_email_2', models.EmailField(max_length=254, null=True)),
                ('contact_phone_1', models.CharField(max_length=255, null=True)),
                ('contact_phone_2', models.CharField(max_length=255, null=True)),
                ('location_text', models.CharField(max_length=255, null=True)),
                ('location_info', models.CharField(max_length=255, null=True)),
                ('location_street', models.CharField(max_length=255, null=True)),
                ('location_city_subsection', models.CharField(max_length=255, null=True)),
                ('location_neighborhood', models.CharField(max_length=255, null=True)),
                ('location_municipality', models.CharField(max_length=255, null=True)),
                ('location_sub_province', models.CharField(max_length=255, null=True)),
                ('location_province', models.CharField(max_length=255, null=True)),
                ('location_postal_code_1', models.CharField(max_length=255, null=True)),
                ('location_nation', models.CharField(max_length=255, null=True)),
                ('train_lines', models.CharField(max_length=255, null=True)),
                ('bus_lines', models.CharField(max_length=255, null=True)),
                ('world_id', models.CharField(max_length=255, null=True)),
                ('comments', models.CharField(max_length=255, null=True)),
                ('meeting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='RootServer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ServiceBody',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('source_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('AS', 'Area'), ('MA', 'Metro'), ('RS', 'Region')], max_length=2)),
                ('description', models.TextField(null=True)),
                ('url', models.URLField(null=True)),
                ('world_id', models.CharField(max_length=255, null=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.ServiceBody')),
                ('root_server', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.RootServer')),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='root_server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.RootServer'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='service_body',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.ServiceBody'),
        ),
        migrations.AddField(
            model_name='importproblem',
            name='root_server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.RootServer'),
        ),
        migrations.AddField(
            model_name='format',
            name='root_server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.RootServer'),
        ),
    ]

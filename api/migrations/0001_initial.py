# Generated by Django 4.0.10 on 2023-06-14 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('regdno', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]

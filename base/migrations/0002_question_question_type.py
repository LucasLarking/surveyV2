# Generated by Django 4.1.2 on 2022-10-21 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

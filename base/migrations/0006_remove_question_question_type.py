# Generated by Django 4.1.2 on 2022-10-21 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_rename_q_type_question_question_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_type',
        ),
    ]

# Generated by Django 4.1.2 on 2022-10-21 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_question_giveotherfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='giveOtherField',
        ),
    ]
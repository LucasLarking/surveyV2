# Generated by Django 4.1.2 on 2022-11-02 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_remove_question_otherfield_question_showotherfield_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='vote',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(blank=True, choices=[('radio', 'radio'), ('checkbox', 'checkbox')], default='radio', max_length=200, null=True),
        ),
    ]

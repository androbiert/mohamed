# Generated by Django 4.2.3 on 2023-10-19 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_remove_choice_question_question_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='choice',
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='polls.question'),
            preserve_default=False,
        ),
    ]

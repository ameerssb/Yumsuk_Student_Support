# Generated by Django 4.0.6 on 2023-01-30 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_remove_answercomment_comment_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='question.question'),
            preserve_default=False,
        ),
    ]
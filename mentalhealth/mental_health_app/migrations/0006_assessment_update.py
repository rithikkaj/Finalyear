# Generated manually for assessment model update

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mental_health_app', '0005_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessment',
            name='anxiety_level',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='depression_level',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='occupation',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='course',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='stream',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='anxiety_range',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='depression_range',
        ),
        migrations.AddField(
            model_name='assessment',
            name='anxiety_score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assessment',
            name='depression_score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assessment',
            name='responses',
            field=models.JSONField(default=dict),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-09 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comparasion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='soccer',
            name='total_odds_over',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='soccer',
            name='total_odds_under',
            field=models.IntegerField(null=True),
        ),
    ]

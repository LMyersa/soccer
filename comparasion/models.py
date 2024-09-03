import uuid
from django.db import models

# Create your models here.
# class Soccer(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     match_date = models.DateField()
#     match_time = models.TimeField()
#     match_title = models.CharField(max_length=100)
#     player_name = models.CharField(max_length=100)
#     stat_name = models.CharField(max_length=100)
#     stat_value = models.FloatField()
#     stat_type = models.CharField(max_length=100)
#     over_multiplier = models.FloatField(null=True)
#     under_multiplier = models.FloatField(null=True)
#     bet365_over_odds = models.IntegerField(null=True)
#     bet365_under_odds = models.IntegerField(null=True)
#     kambi_over_odds = models.IntegerField(null=True)
#     kambi_under_odds = models.IntegerField(null=True)
#     total_odds_over = models.IntegerField(null=True)
#     total_odds_under = models.IntegerField(null=True)
#
#     def __str__(self):
#         return str(f"{self.player_name} - {self.stat_name}")

class OverOdds(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    match_date = models.DateField()
    match_time = models.TimeField()
    match_title = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100)
    stat_name = models.CharField(max_length=100)
    stat_value = models.FloatField()
    stat_type = models.CharField(max_length=100)
    over_multiplier = models.FloatField(null=True)
    bet365_over_odds = models.IntegerField(null=True)
    kambi_over_odds = models.IntegerField(null=True)
    total_odds_over = models.IntegerField(null=True)

    def __str__(self):
        return str(f"{self.player_name} - {self.stat_name}")


class UnderOdds(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    match_date = models.DateField()
    match_time = models.TimeField()
    match_title = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100)
    stat_name = models.CharField(max_length=100)
    stat_value = models.FloatField()
    stat_type = models.CharField(max_length=100)
    under_multiplier = models.FloatField(null=True)
    bet365_under_odds = models.IntegerField(null=True)
    kambi_under_odds = models.IntegerField(null=True)
    total_odds_under = models.IntegerField(null=True)

    def __str__(self):
        return str(f"{self.player_name} - {self.stat_name}")
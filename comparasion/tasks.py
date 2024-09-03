from Soccer.celery import app
from comparasion.models import OverOdds, UnderOdds
from comparasion.Comparasion_Util import Compare
from django.db import transaction


@app.task
def task_one():
    print(" task one called and worker is running good")
    return "success"


@app.task
def task_two(data, *args, **kwargs):
    print(f" task two called with the argument {data} and worker is running good")
    return "success"


@app.task
@transaction.atomic
def add_data_util():
    OverOdds.objects.all().delete()
    UnderOdds.objects.all().delete()

    comparison = Compare()
    comparison.run_comparisons_concurrently()
    combined_data = comparison.combined_data

    over_odds_objects_to_create = []
    under_odds_objects_to_create = []
    over_batch_size = 100
    under_batch_size = 100

    for data in combined_data:
        match_date = data["game_date"]
        match_time = data["game_time"]
        match_title = data["match_name"]
        player_name = data["full_name"]

        for stat in data["stats"]:
            stat_name = stat["stat_title"]
            stat_value = float(stat["stat_value"])
            over_multiplier = stat["underdog_stat"]["over_multiplier"]
            under_multiplier = stat["underdog_stat"]["under_multiplier"]

            # Initialize odds variables for over and under separately
            bet365_over_odds = None
            kambi_over_odds = None
            bet365_under_odds = None
            kambi_under_odds = None
            total_over_odds = None
            total_under_odds = None

            # Process each stat type separately
            for bet365 in stat.get("bet365_stat", []):
                if bet365["stat_type"] == "Over":
                    bet365_over_odds = bet365["american_odds"]
                elif bet365["stat_type"] == "Under":
                    bet365_under_odds = bet365["american_odds"]

            for kambi in stat.get("kambi_stat", []):
                if kambi["stat_type"] == "Over":
                    kambi_over_odds = kambi["american_odds"]
                elif kambi["stat_type"] == "Under":
                    kambi_under_odds = kambi["american_odds"]

            if bet365_over_odds is not None and kambi_over_odds is not None:
                total_over_odds = bet365_over_odds + kambi_over_odds

            if bet365_under_odds is not None and kambi_under_odds is not None:
                total_under_odds = bet365_under_odds + kambi_under_odds

            if bet365_over_odds is not None or kambi_over_odds is not None:
                over_odds_objects_to_create.append(OverOdds(
                    match_date=match_date,
                    match_time=match_time,
                    match_title=match_title,
                    player_name=player_name,
                    stat_name=stat_name,
                    stat_value=stat_value,
                    stat_type="Over",
                    over_multiplier=over_multiplier,
                    bet365_over_odds=bet365_over_odds,
                    kambi_over_odds=kambi_over_odds,
                    total_odds_over=total_over_odds,
                ))

            if bet365_under_odds is not None or kambi_under_odds is not None:
                under_odds_objects_to_create.append(UnderOdds(
                    match_date=match_date,
                    match_time=match_time,
                    match_title=match_title,
                    player_name=player_name,
                    stat_name=stat_name,
                    stat_value=stat_value,
                    stat_type="Under",
                    under_multiplier=under_multiplier,
                    bet365_under_odds=bet365_under_odds,
                    kambi_under_odds=kambi_under_odds,
                    total_odds_under=total_under_odds,
                ))

    OverOdds.objects.bulk_create(over_odds_objects_to_create, batch_size=over_batch_size)
    UnderOdds.objects.bulk_create(under_odds_objects_to_create, batch_size=under_batch_size)


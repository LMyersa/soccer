from django.db.models import Q
from django.shortcuts import render
from comparasion.add_data_util import add_data_util
# from comparasion.models import Soccer
from comparasion.models import OverOdds, UnderOdds
from itertools import chain

def load_comparasion(request, filter_type):
    add_data_util()

    if filter_type == "filter":
        over_odds_player = OverOdds.objects.filter(
            over_multiplier__isnull=False,
            over_multiplier__gt=0.99,
            total_odds_over__isnull=False
        )
        under_odds_player = UnderOdds.objects.filter(
            under_multiplier__isnull=False,
            under_multiplier__gt=0.99,
            total_odds_under__isnull=False
        )
        combined_players = list(chain(over_odds_player, under_odds_player))
        player = sorted(combined_players, key=custom_sort_key)
    elif filter_type == "day-filter":
        over_odds_player = OverOdds.objects.filter(
            over_multiplier__isnull=False,
            over_multiplier__gt=0.99,
            total_odds_over__isnull=False
        ).order_by('match_date')
        under_odds_player = UnderOdds.objects.filter(
            under_multiplier__isnull=False,
            under_multiplier__gt=0.99,
            total_odds_under__isnull=False
        ).order_by('match_date')

        combined_player = list(chain(over_odds_player, under_odds_player))
        player = sorted(combined_player, key=lambda x: x.match_date)
    elif filter_type == "multi-filter":
        over_odds_player = OverOdds.objects.filter(
            over_multiplier__isnull=False,
            over_multiplier__gt=1,
            total_odds_over__isnull=False
        ).order_by('match_date')
        under_odds_player = UnderOdds.objects.filter(
            under_multiplier__isnull=False,
            under_multiplier__gt=1,
            total_odds_under__isnull=False
        ).order_by('match_date')

        combined_players = list(chain(over_odds_player, under_odds_player))
        player = sorted(combined_players, key=custom_sort_key)

    else:
        over_odds_player = OverOdds.objects.filter(
            over_multiplier__isnull=False,
        )
        under_odds_player = UnderOdds.objects.filter(
            under_multiplier__isnull=False,
        )
        player = list(chain(over_odds_player, under_odds_player))

    context={"player": player}

    return render(request, 'comparasion.html', context)

def home(request):
    return render(request, 'home.html')


def custom_sort_key(player):
    # Check for 'total_odds_over' attribute, if it exists, sort by it; otherwise, sort by 'total_odds_under'
    return getattr(player, 'total_odds_over', None) if hasattr(player, 'total_odds_over') else getattr(player, 'total_odds_under', None)
from django.db.models import Q
from .models import OverOdds, UnderOdds
from itertools import chain

def total_count_context(request):
    # Logic for filtered count
    filter_over_odds_player = OverOdds.objects.filter(
        over_multiplier__isnull=False,
        over_multiplier__gt=0.99,
        total_odds_over__isnull=False
    )
    filter_under_odds_player = UnderOdds.objects.filter(
        under_multiplier__isnull=False,
        under_multiplier__gt=0.99,
        total_odds_under__isnull=False
    )

    filter_combined_players = list(chain(filter_over_odds_player, filter_under_odds_player))
    filter_count = len(filter_combined_players)

    # Logic for non-filtered count
    non_filter_over_odds_player = OverOdds.objects.filter(
        over_multiplier__isnull=False,
    )
    non_filter_under_odds_player = UnderOdds.objects.filter(
        under_multiplier__isnull=False,
    )
    non_filter_combined_players = list(chain(non_filter_over_odds_player, non_filter_under_odds_player))
    non_filter_count = len(non_filter_combined_players)

    return {'filter_count': filter_count, 'non_filter_count': non_filter_count}

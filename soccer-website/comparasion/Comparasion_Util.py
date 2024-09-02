import json
from threading import Thread
from comparasion.Underdog_Util import Underdog
from comparasion.Oddschecker_Util import OddsChecker



class Compare():
    def __init__(self):
        self.underdog_data = self.get_underdog_data()
        self.bet365_data, self.kambi_data = self.get_odds_checker_data()
        self.combined_data = []

    def get_underdog_data(self):
        ud = Underdog(["FIFA", "SOCCER"])
        ud.get_player_information(ud.get_underdog_data(filter_word="players"))
        ud.get_ids(ud.get_underdog_data(filter_word="appearances"))
        ud.get_time_date(ud.get_underdog_data(filter_word="games"))
        ud.get_player_stats(underdog_data=ud.get_underdog_data(filter_word="over_under_lines"),
                            stat_type=["shots attempted", "shots on target"])
        ud.filter_players_by_stats(["Player Shots", "Player Shots On Target"])

        return ud.player_stats

    def get_odds_checker_data(self):
        od = OddsChecker()
        od.get_event_id()
        od.get_shot_id()
        od.get_player_stats(od.get_shot_id_list(), [(od.bet365_stats, "B3"), (od.kambi_stats, "UN")])
        od.filter_non_bookmakers(((od.bet365_stats, "Bet365"), (od.kambi_stats, "Kambi")))

        return od.bet365_filtered_stats, od.kambi_filtered_stats

    def compare_bookmaker(self, bookmaker_data, stat_key):
        for ud_player in self.underdog_data:
            for bookmaker_player in bookmaker_data:
                if ud_player["full_name"] == bookmaker_player["full_name"]:
                    for ud_stat in ud_player["stats"]:
                        for bookmaker_stat in bookmaker_player["stats"]:
                            if ud_stat["stat_title"] == bookmaker_stat["stat_title"] and ud_stat["stat_value"] == bookmaker_stat["stat_value"]:
                                player_found = False
                                stat_found = False

                                for combined_player in self.combined_data:
                                    if combined_player["full_name"] == ud_player["full_name"]:
                                        player_found = True

                                        for combined_stat in combined_player["stats"]:
                                            if combined_stat["stat_title"] == ud_stat["stat_title"] and combined_stat[
                                                "stat_value"] == ud_stat["stat_value"]:
                                                stat_found = True
                                                secondary_stat_found = False

                                                if stat_key in combined_stat:
                                                    for existing_stat in combined_stat[stat_key]:
                                                        if existing_stat["stat_type"] == bookmaker_stat["stat_type"]:
                                                            secondary_stat_found = True
                                                            break

                                                if not secondary_stat_found:
                                                    combined_stat.setdefault(stat_key, []).append({
                                                        "stat_type": bookmaker_stat["stat_type"],
                                                        "american_odds": bookmaker_stat["american_odds"],
                                                        "bookmaker": bookmaker_stat["bookmaker"],
                                                    })
                                                break

                                        if not stat_found:
                                            combined_player["stats"].append({
                                                "stat_title": ud_stat["stat_title"],
                                                "stat_value": ud_stat["stat_value"],
                                                "underdog_stat": {
                                                    "over_multiplier": ud_stat["over_multiplier"],
                                                    "under_multiplier": ud_stat["under_multiplier"],
                                                },
                                                stat_key: [
                                                    {
                                                        "stat_type": bookmaker_stat["stat_type"],
                                                        "american_odds": bookmaker_stat["american_odds"],
                                                        "bookmaker": bookmaker_stat["bookmaker"],
                                                    }
                                                ]
                                            })
                                        break

                                if not player_found:
                                    self.combined_data.append({
                                        "full_name": ud_player["full_name"],
                                        "match_name": bookmaker_player["match_name"],
                                        "game_date": ud_player["game_date"],
                                        "game_time": ud_player["game_time"],
                                        "stats": [
                                            {
                                                "stat_title": ud_stat["stat_title"],
                                                "stat_value": ud_stat["stat_value"],
                                                "underdog_stat": {
                                                    "over_multiplier": ud_stat["over_multiplier"],
                                                    "under_multiplier": ud_stat["under_multiplier"],
                                                },
                                            }
                                        ]
                                    })

    def run_comparisons_concurrently(self):
        # Create threads for each bookmaker comparison
        thread_bet365 = Thread(target=self.compare_bookmaker, args=(self.bet365_data, "bet365_stat"))
        thread_kambi = Thread(target=self.compare_bookmaker, args=(self.kambi_data, "kambi_stat"))

        # Start the threads
        thread_bet365.start()
        thread_kambi.start()

        # Wait for both threads to complete
        thread_bet365.join()
        thread_kambi.join()









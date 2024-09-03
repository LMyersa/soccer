import requests

class Underdog():
    def __init__(self, sport_ids:list):
        self.sport_ids = sport_ids
        self.player_information = []
        self.player_stats = []


    def get_underdog_data(self, filter_word=None):
        if filter_word is None:
            return requests.get("https://api.underdogfantasy.com/beta/v5/over_under_lines").json()
        else:
            return requests.get("https://api.underdogfantasy.com/beta/v5/over_under_lines").json()[filter_word]


    def get_player_information(self, underdog_data):
        # This will work for everything but ESPORTS as match type is listed as players first name.

        for player in underdog_data:
            if player["sport_id"] in self.sport_ids:
                self.player_information.append({
                    "first_name": player["first_name"],
                    "last_name": player["last_name"],
                    "full_name": player["last_name"] if player["first_name"] == "" else f"{player['first_name']} {player['last_name']}",
                    "sport_id": player["sport_id"],
                    "player_id": player["id"],
                })


    def get_ids(self, underdog_data):
        for id in underdog_data:
            for player in self.player_information:
                if id["player_id"] == player["player_id"]:
                    player["match_id"] = id["match_id"]
                    player["appearance_id"] = id["id"]
                    break

    def get_time_date(self, underdog_data):
        for time in underdog_data:
            for player in self.player_information:
                if player["match_id"] == time["id"]:

                    time_date_split = time["scheduled_at"].split("T")
                    game_date = time_date_split[0]
                    game_time = time_date_split[1][:-1]

                    player["game_date"] = game_date
                    player["game_time"] = game_time


    def get_player_stats(self, underdog_data, stat_type):
        for player in self.player_information:
            for stat in underdog_data:
                if player["appearance_id"] == stat["over_under"]["appearance_stat"]["appearance_id"] and stat["over_under"]["appearance_stat"]["display_stat"].lower() in stat_type:
                    over_multiplier, under_multiplier = None, None

                    for option in stat["options"]:
                        if option["choice"] == "higher":
                            over_multiplier = float(option["payout_multiplier"])
                        elif option["choice"] == "lower":

                            under_multiplier = float(option["payout_multiplier"]) if option["payout_multiplier"] != None else \
                            float(option["payout_multiplier"])

                    stat_title = f"Player {stat['over_under']['appearance_stat']['display_stat'].title()}" \
                        if stat["over_under"]["appearance_stat"]["display_stat"] == "Shots on Target" \
                        else "Player Shots"

                    if "stats" in player:
                        player["stats"].append({
                            "stat_title": stat_title,
                            "stat_value": stat["stat_value"],
                            "over_multiplier": over_multiplier,
                            "under_multiplier": under_multiplier,

                        })
                    else:
                        player["stats"] = [{
                            "stat_title": stat_title,
                            "stat_value": stat["stat_value"],
                            "over_multiplier": over_multiplier,
                            "under_multiplier": under_multiplier,
                        }]


    def filter_players_by_stats(self, filtered_words):
        filtered_words_lower = [word.lower() for word in filtered_words]

        for word in filtered_words_lower:
            for data in self.player_information:
                stats = data.get("stats")
                if stats:  # Proceed only if 'stat' key exists and is not None
                    for stat in stats:
                        if word == stat["stat_title"].lower():
                            self.player_stats.append(data)
                            break


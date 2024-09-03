import json
import threading
import requests
import tls_client
from fake_useragent import UserAgent


class OddsChecker():
    def __init__(self):
        self.leagues = self.get_leagues()
        self.league_data = []
        self.lock = threading.Lock()
        self.bet365_stats = []
        self.kambi_stats = []
        self.bet365_filtered_stats = []
        self.kambi_filtered_stats = []

    def get_leagues(self):
        # EVENT ID FOR LEAGUES
        return {
            "English Premier League": 2457,
            "English Championship": 9961,
            "Europa League": 10545,
            "Championship League": 218309,
            "FA Cup": 5231,
            "League One": None,
            "League Two": 9962,
            "Euro 2024": 38992229,
            "UEFA Europa Conference League": 38925767,
            "Friendlies": None,
            "Scottish Premiership": 2463,
            "Bundesliga": None,
            "Bundesliga 2": 9936,
            "Serie A": 9950,
            "La Liga Primera": 9945,
            "Copa America": 54728,
            "US Major League Soccer": 197296,
            "French Ligue 1": 9941,
        }

    def get_event_api_data(self, event_id, league):
        url = f"https://api.oddschecker.com/bet-builder/v1/events/{event_id}/subevents"
        headers = {
            "Accept": "application/json",
            "API-KEY": "d6f0f240-dbe4-40eb-a133-63a6d81191e6",
            "Connection": "keep-alive",
            "Host": "api.oddschecker.com",
            "Origin": "https://www.oddschecker.com",
            "Referer": "https://www.oddschecker.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
        }

        response = requests.get(url, headers=headers).json()

        if "subevents" in response:
            with self.lock:
                for event in response["subevents"]:
                    self.league_data.append({
                        "league": league,
                        "event_id": event["id"],
                        "match_name": event["name"],
                        "time": event["startTime"],
                    })

    def fetch_events(self):
        threads = []
        for league, event_id in self.leagues.items():
            if event_id:  # Check if event_id is not None
                thread = threading.Thread(target=self.get_event_api_data, args=(event_id, league))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

    def get_event_id(self):
        self.fetch_events()

    def get_shot_data(self, dictionary_data):
        url = f"https://api.oddschecker.com/bet-builder/v1/subevents/{dictionary_data['event_id']}/markets"
        payload = ""
        headers = {
            "cookie": "__cf_bm=x8RXuiWcD.vHjl8h3ZE0W.x82Qv1EQn5lyG12LPt8tw-1720280960-1.0.1.1-0LQ146ZoaTnaZOtogOwFzZdIu6JiZOTIHfyesgiQBxgABhZ5vrRlwOyjwbYzt0GWD1pTzwq5QUPpKhpZPrm3oA",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
            "Accept": "application/json",
            "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://www.oddschecker.com/",
            "API-KEY": "d6f0f240-dbe4-40eb-a133-63a6d81191e6",
            "Origin": "https://www.oddschecker.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=4",
            "TE": "trailers"
        }

        response = requests.request("GET", url, data=payload, headers=headers).json()

        if response:
            for r in response["markets"]:
                if "Player Shots On Target" == r["name"] or "Player Shots" == r["name"]:
                    with self.lock:
                        dictionary_data.update({
                            f"{r['name']} ID": r["id"]
                        })

    def fetch_shots(self):
        threads = []

        for league_data in self.league_data:
            thread = threading.Thread(target=self.get_shot_data, args=(league_data,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def get_shot_id(self):
        self.fetch_shots()

    def get_player_stats_odds(self, event_id, bookmaker_stat, bookmaker_code):
        ua = UserAgent(os='ios')  # Narrow this to iOS
        user_agent = ua.random  # Generate a random user-agent

        url = f"https://www.oddschecker.com/api/markets/v2/all-odds?market-ids={event_id}&repub=OC"

        # Basic headers
        headers = {
            'accept': '*/*',
            'User-Agent': user_agent,
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Origin': 'https://www.oddschecker.com'
        }

        session = tls_client.Session(client_identifier="safari_ios_16_0")
        response = session.get(url, headers=headers).json()

        for data in response:
            stat_title = data["marketTypeName"]
            for bet in data["bets"]:
                split_name = bet["betName"].split(" ")
                name = split_name[:-1]
                stat_type = split_name[-1]
                full_name = " ".join(name) if len(name) > 1 else name[0]
                bet_id = bet["betId"]


                odds_value = None
                bookmaker = None
                american_odds = None

                for odds in data["odds"]:
                    if bet_id == odds["betId"]:
                        if odds["bookmakerCode"] == bookmaker_code and odds["status"] == "ACTIVE":
                            odds_value = odds["oddsDecimal"]
                            bookmaker = "Bet365" if bookmaker_code == "B3" else "Kambi"

                            if odds_value is not None:
                                american_odds = self.odds_conversion(odds_value)

                player_found = False
                for player_data in bookmaker_stat:
                    if player_data["full_name"] == full_name:
                        player_data["stats"].append({
                            "stat_title": stat_title,
                            "stat_type": stat_type,
                            "stat_value": bet["line"],
                            "id": bet["betId"],
                            "decimal_odds": odds_value,
                            "american_odds": american_odds,
                            "bookmaker": bookmaker,
                        })
                        player_found = True
                        break

                if not player_found:
                    bookmaker_stat.append({
                        "full_name": full_name,
                        "match_name": data["subeventName"],
                        "stats": [{
                            "stat_title": stat_title,
                            "stat_type": stat_type,
                            "stat_value": bet["line"],
                            "id": bet["betId"],
                            "decimal_odds": odds_value,
                            "american_odds": american_odds,
                            "bookmaker": bookmaker,
                        }]
                    })

    def odds_conversion(self, odds):
        if odds >= 2:
            return round((odds - 1) * 100)
        else:
            return round(-100 / (odds - 1))

    def get_shot_id_list(self):
        shot_id_list = []
        for id in self.league_data:
            if "Player Shots On Target ID" in id:
                shot_id_list.append(id["Player Shots On Target ID"])
            if "Player Shots ID" in id:
                shot_id_list.append(id["Player Shots ID"])
        return shot_id_list

    def fetch_player_stats(self, ids, bookmaker_stat, bookmaker_code):
        threads = []

        for id in ids:
            thread = threading.Thread(target=self.get_player_stats_odds, args=(id, bookmaker_stat, bookmaker_code))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def get_player_stats(self, ids, bookmaker_stats_codes):
        threads = []

        for bookmaker_stat, bookmaker_code in bookmaker_stats_codes:
            thread = threading.Thread(target=self.fetch_player_stats, args=(ids, bookmaker_stat, bookmaker_code))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


    def filter_non_bookmakers(self, bookmaker_stats_tuples):
        for bookmaker_stats, bookmaker_name in bookmaker_stats_tuples:
            filtered_stats = []
            for player in bookmaker_stats:
                # Filter stats based on the bookmaker
                player_filtered_stats = [stat for stat in player.get("stats", []) if
                                         stat["bookmaker"] == bookmaker_name]
                if player_filtered_stats:
                    filtered_player = player.copy()
                    filtered_player["stats"] = player_filtered_stats
                    filtered_stats.append(filtered_player)

            # Save the filtered stats to the corresponding attribute based on the bookmaker
            if bookmaker_name == "Kambi":
                self.kambi_filtered_stats.extend(filtered_stats)
            elif bookmaker_name == "Bet365":
                self.bet365_filtered_stats.extend(filtered_stats)


import requests
from dotenv import load_dotenv
from pprint import pprint
from mongodb import get_most_recent_token
import os

load_dotenv()

TOKEN = get_most_recent_token()
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}


class Ship:
    def __init__(self, header, ship_id):
        self.header = header
        self.ship_id = ship_id

    def __repr__(self):
        ship = self.get_ship_info()
        ship_status = ship["nav"]["status"]
        ship_symbol = ship["symbol"]
        return (
            f"Ship_ID: {self.ship_id}"
            "\n"
            f"Ship Symbol: {ship_symbol}"
            "\n"
            f"Status: {ship_status}"
        )

    def get_ship_info(self):
        request = requests.get(
            f"https://api.spacetraders.io/v2/my/ships/", headers=self.header
        )
        return request.json()["data"][self.ship_id]

    def all_ship_info(self):
        request = requests.get(
            f"https://api.spacetraders.io/v2/my/ships/", headers=self.header
        )
        return request.json()["data"]

    def dock_or_orbit(self):
        ship = self.get_ship_info(self)
        ship_status = ship["nav"]["status"]
        ship_symbol = ship["symbol"]
        if ship_status == "DOCKED":
            request = requests.post(
                f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/orbit",
                headers=self.header,
            )
        if ship_status == "IN_ORBIT":
            request = requests.post(
                f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/dock",
                headers=self.header,
            )

        return request.json()["data"]["nav"]["status"]

    def navigate_ship(self, waypoint):
        ship = self.get_ship_info()["symbol"]
        data = {"waypointSymbol": waypoint}
        request = requests.post(
            f"https://api.spacetraders.io/v2/my/ships/{ship}/navigate",
            headers=self.header,
            json=data,
        )
        return request.json()["data"]["nav"]


ship = Ship(HEADERS, 0)


import matplotlib.pyplot as plt
import numpy as np
import requests
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get("TOKEN")

HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}


def get_systems(header):
    request = requests.get("https://api.spacetraders.io/v2/systems", headers=header)
    try:
        return request.json()["data"]
    except:
        return request.json()["error"]


def show_system():
    systems = get_systems(HEADERS)

    for system in systems:
        x = system["x"]
        y = system["y"]
        plt.scatter(x, y)
        label = system["symbol"]
        plt.annotate(label, (x, y))

    plt.show()


def print_system_info(header):
    systems = get_systems(header)
    for system in systems:
        print("\n")
        for body in system["waypoints"]:
            print(body)


print_system_info(HEADERS)

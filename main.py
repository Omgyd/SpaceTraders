import requests
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get("TOKEN")
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}


def register():
    header = {"Content-Type": "application/json"}
    payload = {
        "symbol": "RAVENOR",
        "faction": "COSMIC",
    }

    request = requests.post(
        "https://api.spacetraders.io/v2/register", headers=header, json=payload
    )
    return request.json()


def my_agent_info(header):
    request = requests.get("https://api.spacetraders.io/v2/my/agent", headers=header)
    return request.json()


def view_contract(header):
    request = requests.get(
        "https://api.spacetraders.io/v2/my/contracts", headers=header
    )
    return request.json()["data"]


def accept_contract(header, contract_id):
    request = requests.post(
        f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/accept",
        headers=header,
    )
    return request.json()


def get_ship_info(header, ship_number):
    request = requests.get(f"https://api.spacetraders.io/v2/my/ships/", headers=header)
    return request.json()["data"][ship_number]


def all_ship_info(header):
    request = requests.get(f"https://api.spacetraders.io/v2/my/ships/", headers=header)
    return request.json()["data"]


def get_systems(header):
    request = requests.get("https://api.spacetraders.io/v2/systems", headers=header)
    return request.json()


def check_system(header):
    system = my_agent_info(header)
    system_symbol = system["data"]["headquarters"].split("-")
    request = requests.get(
        f"https://api.spacetraders.io/v2/systems/{system_symbol[0]}-{system_symbol[1]}/waypoints/",
        headers=header,
    )
    return request.json()["data"]


def check_waypoints(header):
    request = requests.get(f"https://api.spacetraders.io/v2/systems/X1-YU85/waypoints")
    return request.json()


def find_shipyard(header):
    system = check_system(header)

    for item in system:
        for trait in item["traits"]:
            if trait["symbol"] == "SHIPYARD":
                return item["symbol"]


def view_ships(header):
    waypoint = find_shipyard(header)
    system_symbol = waypoint.split("-")
    request = requests.get(
        f"https://api.spacetraders.io/v2/systems/{system_symbol[0]}-{system_symbol[1]}/waypoints/{waypoint}/shipyard"
    )
    return request.json()["data"]


# shipyard = get_location(HEADERS)
# for ship in shipyard['data']['ships']:
#     print(ship)

# data = {
#     "shipType": "SHIP_MINING_DRONE",
#     "waypointSymbol": "X1-YU85-34607X"
# }

# request = requests.post('https://api.spacetraders.io/v2/my/ships', headers=HEADERS, json=data)
# print(request.json())
# ships = get_ship_info(HEADERS)['data']
# print(ships[3])

# Find asteroid fileds in current system
# for item in traits:
#     if item['type'] == 'ASTEROID_FIELD':
#         print(item['symbol'])


def dock_or_orbit(header, ship_number):
    ship = get_ship_info(header, ship_number)
    ship_status = ship["nav"]["status"]
    ship_symbol = ship["symbol"]
    if ship_status == "DOCKED":
        request = requests.post(
            f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/orbit",
            headers=header,
        )
    if ship_status == "IN_ORBIT":
        request = requests.post(
            f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/dock",
            headers=header,
        )

    return request.json()["data"]["nav"]["status"]


def navigate_ship(header):
    ship = "RAVENOR-4"
    data = {"waypointSymbol": "X1-YU85-76885D"}
    request = requests.post(
        f"https://api.spacetraders.io/v2/my/ships/{ship}/navigate",
        headers=header,
        json=data,
    )
    return request.json()["data"]["nav"]["status"]


# for item in get_ship_info(HEADERS)['data'][3]:
#     print(item)


def extract_ore(header, ship_number):
    ship = get_ship_info(header, ship_number)
    ship_symbol = ship["symbol"]
    request = requests.post(
        f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/extract", headers=header
    )

    try:
        info = request.json()["data"]
        print(
            f"Yield: {info['extraction']['yield']['symbol']} - {info['extraction']['yield']['units']} Units"
        )
        print(f'Cooldown Time: {info["cooldown"]["totalSeconds"]}')
        return info["cooldown"]["totalSeconds"]
    except:
        return request.json()["error"]


# for ship in get_ship_info(HEADERS):
#     print(ship['registration'], "\n", ship['nav'], "\n")


def get_market_data(header):
    system_symbol = "X1-YU85"
    waypoint = "X1-YU85-34607X"
    request = requests.get(
        f"https://api.spacetraders.io/v2/systems/{system_symbol}/waypoints/{waypoint}/market"
    )
    return request.json()["data"]


def get_ship_cargo(header, ship_number):
    ship_symbol = get_ship_info(header, ship_number)["symbol"]
    request = requests.get(
        f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/cargo", headers=header
    )
    ship = request.json()["data"]
    for item in ship:
        if item == "inventory":
            print("\n")
            for cargo in ship["inventory"]:
                print(f"{cargo['name']}: {cargo['units']}")
        else:
            print(f"{item.title()}: {ship[item]}")


def sell_all_cargo(header, ship_number):
    ship = get_ship_info(header, ship_number)
    ship_symbol = ship["symbol"]
    for cargo in ship["cargo"]["inventory"]:
        data = {}
        data["symbol"] = cargo["symbol"]
        data["units"] = cargo["units"]
        request = requests.post(
            f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/sell",
            headers=header,
            json=data,
        )
        print(request.json())


def extract_all_ore():
    ship = get_ship_info(HEADERS, 3)["cargo"]
    ship_capacity = ship["capacity"]
    ship_units = ship["units"]
    while ship_units != ship_capacity:
        sleep(extract_ore(HEADERS, 3))


def auto_mine(header, ship_number):
    credits = my_agent_info(header)
    print(credits)

import requests
from time import sleep
from dotenv import load_dotenv
from mongodb import get_most_recent_token, insert_token
from pprint import pprint
from ships import Ship
import os

load_dotenv()

TOKEN = get_most_recent_token()
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}


def register(name):
    header = {"Content-Type": "application/json"}
    payload = {
        "symbol": name,
        "faction": "COSMIC",
    }

    request = requests.post(
        "https://api.spacetraders.io/v2/register", headers=header, json=payload
    )
    token = request.json()['data']['token']
    insert_token(token)


def my_agent_info(header):
    request = requests.get("https://api.spacetraders.io/v2/my/agent", headers=header)
    return request.json()


def view_contract(header):
    request = requests.get(
        "https://api.spacetraders.io/v2/my/contracts", headers=header
    )
    return request.json()


def accept_contract(header):
    contract_id = view_contract(header)['data'][0]['id']
    request = requests.post(
        f"https://api.spacetraders.io/v2/my/contracts/{contract_id}/accept",
        headers=header,
    )
    return request.json()


def get_ship_info(header, ship_number):
    request = requests.get(f"https://api.spacetraders.io/v2/my/ships/", headers=header)
    try:
        return request.json()["data"][ship_number]
    except:
        return request.json()


def all_ship_info(header):
    request = requests.get(f"https://api.spacetraders.io/v2/my/ships/", headers=header)
    return request.json()["data"]


def get_systems(header):
    request = requests.get("https://api.spacetraders.io/v2/systems", headers=header)
    return request.json()

def scan_waypoints(header, ship_id):
    ship = get_ship_info(header, ship_id)
    ship_status = ship['nav']['status']
    ship_symbol = ship['symbol']
    if ship_status == "DOCKED":
        dock_or_orbit(header, ship_id)
    request = requests.post(f'https://api.spacetraders.io/v2/my/ships/{ship_symbol}/scan/waypoints', headers=header)
    try:
        return request.json()['data']
    except:
        return request.json()['error']


def check_system(header):
    system = my_agent_info(header)
    system_symbol = system["data"]["headquarters"].split("-")
    request = requests.get(
        f"https://api.spacetraders.io/v2/systems/{system_symbol[0]}-{system_symbol[1]}/waypoints/",
        headers=header,
    )
    return request.json()["data"]



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
    return request.json()

def purchase_ship(header, ship_type):
    waypoint = find_shipyard(HEADERS)
    data = {
        "shipType": ship_type,
        "waypointSymbol": waypoint
    }

    request = requests.post('https://api.spacetraders.io/v2/my/ships', headers=header, json=data)
    return request.json()


def find_asteroid_field(header):
    # Find asteroid fileds in current system
    system = check_system(header)
    for item in system:
        for trait in item['traits']:
            if item['type'] == 'ASTEROID_FIELD':
                return item['symbol']
            
def find_marketplace(header):
    system = check_system(header)

    for item in system:
        for trait in item["traits"]:
            if trait["symbol"] == "MARKETPLACE":
                return item["symbol"]


def check_marketplace(header):
    waypoint = find_marketplace(header)
    system_symbol = waypoint.split("-")
    request = requests.get(f"https://api.spacetraders.io/v2/systems/{system_symbol[0]}-{system_symbol[1]}/waypoints/{waypoint}/market", headers=header)
    return request.json()

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

def navigate_to_shipyard(header, ship_number):
    ship = get_ship_info(header, ship_number)
    ship_symbol = ship['symbol']
    ship_status = ship['nav']['status']
    shipyard = find_shipyard(header)
    data = {"waypointSymbol": shipyard}
    if ship_status == "DOCKED":
        dock_or_orbit(header, ship_number)
    request = requests.post(
        f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/navigate",
        headers=header,
        json=data,
    )
    return request.json()["data"]["nav"]


def navigate_to_asteroid_field(header, ship_number):
    ship = get_ship_info(header, ship_number)
    ship_status = ship['nav']['status']
    ship_symbol = ship['symbol']
    asteroid_field = find_asteroid_field(header)
    data = {"waypointSymbol": asteroid_field}
    if ship_status == "DOCKED":
        dock_or_orbit(header, ship_number)
    request = requests.post(
        f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/navigate",
        headers=header,
        json=data,
    )
    try:
        return request.json()["data"]["nav"]
    except:
        return request.json()['error']

def navigate_to_marketplace(header, ship_number):
        ship = get_ship_info(header, ship_number)
        ship_status = ship['nav']['status']
        ship_symbol = ship['symbol']
        marketplace = find_marketplace(header)
        data = {"waypointSymbol": marketplace}
        if ship_status == "DOCKED":
            dock_or_orbit(header, ship_number)
        request = requests.post(
            f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/navigate",
            headers=header,
            json=data,
        )
        try:
            return request.json()["data"]["nav"]
        except:
            return request.json()['error']['message']

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
        return [info["cooldown"]["totalSeconds"], info['extraction']['yield']['units']]
    except:
        print(request.json()['error']['message'])
        return 0


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
    credits = my_agent_info(header)['data']['credits']
    ship = get_ship_info(header, ship_number)
    ship_symbol = ship["symbol"]
    total_sale = 0
    if ship['cargo']['units'] == 0:
        return "No cargo to sell"
    if ship['nav']['status'] == "IN_ORBIT":
        dock_or_orbit(header, ship_number)
    while ship['cargo']['units'] > 0:
        for cargo in ship["cargo"]["inventory"]:
            data = {}
            data["symbol"] = cargo["symbol"]
            data["units"] = cargo["units"]
            request = requests.post(
                f"https://api.spacetraders.io/v2/my/ships/{ship_symbol}/sell",
                headers=header,
                json=data,
            )
            sale = request.json()['data']['transaction']['totalPrice']
            total_sale += sale
        return total_sale


def extract_all_ore(header, ship_id):
    ship = get_ship_info(header, ship_id)
    ship_status = ship['nav']['status']
    ship_capacity = ship['cargo']["capacity"]
    ship_units = ship['cargo']["units"]
    if ship_units == ship_capacity:
        return "Cargo Full"
    if ship_status == "DOCKED":
        dock_or_orbit(header, ship_id)
    while ship_units < ship_capacity:
        extraction_data = extract_ore(header, ship_id)
        ship_units += extraction_data[1]
        print(f'{ship_units}/{ship_capacity}')
        # if ship_units >= ship_capacity:
        #     break
        sleep(extraction_data[0])
    print("Cargo Full")   


def auto_mine(header, ship_number, target):
    credits = my_agent_info(header)['data']['credits']
    while credits < target:
        print(credits)
        extract_all_ore(header, ship_number)
        sale = sell_all_cargo(header, ship_number)
        credits += sale


# print(accept_contract(HEADERS))
# get_ship_cargo(HEADERS, 2)
# extract_all_ore(HEADERS, 2)
# print(my_agent_info(HEADERS))
# print(sell_all_cargo(HEADERS, 2))
# print(view_ships(HEADERS))


ore_ship = Ship(HEADERS, 0)
# pprint(navigate_to_asteroid_field(HEADERS, 0))
auto_mine(HEADERS, 0, 130000)


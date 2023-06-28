import requests
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get("TOKEN")

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {TOKEN}'
    }

payload = {
    "symbol": "RAVENOR",
    "faction": "COSMIC",
   }

# request = requests.post('https://api.spacetraders.io/v2/register', headers=headers, json=payload)

def my_agent_info(header):
    request = requests.get('https://api.spacetraders.io/v2/my/agent', headers=header)
    return request.json()

def get_contract_id(header):
    request = requests.get('https://api.spacetraders.io/v2/my/contracts', headers=header)
    return request.json()['data'][0]['id']

def accept_contract(header, contract_id):
    request = requests.post(f'https://api.spacetraders.io/v2/my/contracts/{contract_id}/accept', headers=header)
    return request.json()

def get_ship_info(header):
    ship = "RAVENOR-4"
    request = requests.get(f'https://api.spacetraders.io/v2/my/ships/', headers=header)
    return request.json()['data'][3]

def get_systems(header):
    request = requests.get('https://api.spacetraders.io/v2/systems', headers=header)
    return request.json()

def check_system(header):
    system = my_agent_info(header)
    system_symbol = system['data']['headquarters'].split('-')
    request = requests.get(f'https://api.spacetraders.io/v2/systems/{system_symbol[0]}-{system_symbol[1]}/waypoints/', headers=header)
    return request.json()

def check_waypoints(header):
    request = requests.get(f'https://api.spacetraders.io/v2/systems/X1-YU85/waypoints')
    return request.json()



traits = check_waypoints(HEADERS)['data']

# for item in traits:
#     for trait in item['traits']:
#         if trait['symbol'] == "SHIPYARD":
#             print(item['symbol'])



def get_location(header):
    request = requests.get('https://api.spacetraders.io/v2/systems/X1-YU85/waypoints/X1-YU85-34607X/shipyard', headers=header)
    return request.json()


# shipyard = get_location(HEADERS)
# for ship in shipyard['data']['ships']:
#     print(ship)

data = {
    "shipType": "SHIP_MINING_DRONE",
    "waypointSymbol": "X1-YU85-34607X"
}

# request = requests.post('https://api.spacetraders.io/v2/my/ships', headers=HEADERS, json=data)
# print(request.json())
# ships = get_ship_info(HEADERS)['data']
# print(ships[3])

# Find asteroid fileds in current system
# for item in traits:
#     if item['type'] == 'ASTEROID_FIELD':
#         print(item['symbol'])


def send_to_orbit(header):
    request = requests.post('https://api.spacetraders.io/v2/my/ships/RAVENOR-4/orbit', headers=header)
    return request.json()['data']['nav']['status']




def navigate_ship(header):
    ship = "RAVENOR-4"
    data = {"waypointSymbol": "X1-YU85-76885D"}
    request = requests.post(F'https://api.spacetraders.io/v2/my/ships/{ship}/navigate', headers=header, json=data)
    return request.json()['data']['nav']['status']


# for item in get_ship_info(HEADERS)['data'][3]:
#     print(item)

def extract_ore(header):
    ship = "RAVENOR-4"
    request = requests.post(f'https://api.spacetraders.io/v2/my/ships/{ship}/extract', headers=header)
    try:
        return request.json()['data']
    except:
        return request.json()

for system in get_systems(HEADERS)['data']:
    print(system)
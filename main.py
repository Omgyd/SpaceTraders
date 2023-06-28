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
    request = requests.get('https://api.spacetraders.io/v2/my/agent', headers=HEADERS)
    return request.json()

def get_contract_id(header):
    request = requests.get('https://api.spacetraders.io/v2/my/contracts', headers=header)
    return request.json()['data'][0]['id']

def accept_contract(header, contract_id):
    request = requests.post(f'https://api.spacetraders.io/v2/my/contracts/{contract_id}/accept', headers=header)
    return request.json()

def get_ship_info(header,payload):
    request = requests.get(f'https://api.spacetraders.io/v2/my/ships/{payload["symbol"]}/orbit', headers=header)
    return request.json()

def get_systems(header):
    request = requests.get('https://api.spacetraders.io/v2/systems', headers=header)
    return request.json()

def check_system(header):
    system = my_agent_info(header)
    system_symbol = system['data']['headquarters']
    request = requests.get(f'https://api.spacetraders.io/v2/systems/{system_symbol}/waypoints', headers=header)
    return request.json()


print(check_system(HEADERS))




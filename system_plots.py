import matplotlib.pyplot as plt
import numpy as np
import requests
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get("TOKEN")

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {TOKEN}'
    }


def get_systems(header):
    request = requests.get('https://api.spacetraders.io/v2/systems', headers=header)
    try:
        return request.json()['data']
    except:
        return request.json()['error']
# data = {
#     'X1-MS60':{
#     "x": -10301,
#     "y": -12030,
#     },
#     'X1-PV84':{
#     "x": -9357,
#     "y": -9924,
#     }
# }



# for item in data:
#     x = data[item]['x']
#     y = data[item]['y']
#     plt.scatter(x,y)
#     label = item
#     plt.annotate(label, (x,y), textcoords="offset points", ha='center')
    

# plt.show()

def show_system():
    systems = get_systems(HEADERS)

    for system in systems:
        x = system['x']
        y = system['y']
        plt.scatter(x,y)
        label = system["symbol"]
        plt.annotate(label, (x,y))

    plt.show()

systems = get_systems(HEADERS)

for system in systems:
    for body in system['waypoints']:
        print(body)
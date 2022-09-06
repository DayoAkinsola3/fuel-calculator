from flask import Flask, request
import requests
import http.client

app = Flask(__name__)
conn = http.client.HTTPSConnection("api.collectapi.com")
API_KEY = 'apikey 3h9po15E9byeafHcWWE2R3:07cqWNIyDDkVHVKSvMJcyK'


def getGeoLocation(postcode):
    url = f'https://api.postcodes.io/postcodes/{postcode}'
    response = requests.get(url=url)
    data = response.json()
    longitude = data['result']['longitude']
    latitude = data['result']['latitude']
    return {'latitude': latitude, 'longitude': longitude}


@app.route('/fuel-prices')
def getFuelData():
    args = request.args
    postcode = args.get('location')
    fuel_type = args.get('fuelType')
    tank_size = float(args.get('fuelTankSize'))
    coordinates = getGeoLocation(postcode)

    url = 'https://api.collectapi.com/gasPrice/fromCoordinates'

    headers = {'Content-type': "application/json",
               'Authorization': API_KEY}

    params = {'lat': coordinates['latitude'], 'lng': coordinates['longitude'],
              'type': fuel_type}

    response = requests.get(url=url, params=params, headers=headers)

    pricePerLitre = float(response.json()['result']['gasoline'])

    return {"priceForTank": (pricePerLitre * tank_size) * 0.87}

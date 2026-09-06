import requests, sys

header = {"User-Agent": "fetch-weather-cli (grey00man@gmail.com)"}

def get_current_weather(coords: dict) -> dict:
    station_id = _get_observation_station(coords)

    response = requests.get(
        f"https://api.weather.gov/stations/{station_id}/observations/latest",
        headers=header)

    data = response.json()
    if "properties" not in data:
        print("Location not supported by weather.gov.")
        sys.exit()

    return data["properties"]

def _get_observation_station(coords: dict) -> str:
    response = requests.get(
        f"https://api.weather.gov/points/{coords['lat']},{coords['lon']}",
        headers=header)

    data = response.json()
    station_url = data["properties"]["observationStations"]

    response = requests.get(
        station_url, headers=header)

    data = response.json()
    station_id = data["features"][0]["properties"]["stationIdentifier"]

    return station_id
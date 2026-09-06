import requests, sys

def get_address_coordinates(address: str) -> dict:
    response = requests.get(
        "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress", 
        params= {
            "address" : address,
            "benchmark": "Public_AR_Current",
            "format": "json"
        })

    data = response.json()

    if not data["result"]["addressMatches"]:
        print("Geo-lookup requires a street address.")
        sys.exit()

    coords = data["result"]["addressMatches"][0]["coordinates"]

    coords_dict = {
        "lat": coords["y"],
        "lon": coords["x"]
    }

    return coords_dict
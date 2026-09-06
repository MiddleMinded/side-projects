import sys
from geocode import get_address_coordinates
from weather import get_current_weather
from display import print_current_weather

def main():
    address = sys.argv[1]
    coords_dict = get_address_coordinates(address)
    weather_dict = get_current_weather(coords_dict)
    print_current_weather(weather_dict)


if __name__ == "__main__":
    main()
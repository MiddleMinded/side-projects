def print_current_weather(weather_data: dict):
    print(
        f"---Current Weather for {weather_data['stationName']}---\n")

    if weather_data['temperature']['value'] is None:
        temp = "N/A"
    else:
        temp = 	((weather_data['temperature']['value'] * 9/5) + 32)
        temp = f"{round(temp, 1)} F"
    print(f"Temperature: {temp}")

    if not weather_data["cloudLayers"]:
        cl = "N/A"
    else:
        cl = weather_data['cloudLayers'][0]['amount']
        if cl == "SKC" or cl == "CLR":
            cl = "Clear"
        elif cl == "FEW":
            cl = "Mostly Clear"
        elif cl == "SCT":
            cl = "Partly Cloudy"
        elif cl == "BKN":
            cl = "Mostly Cloudy"
        elif cl == "OVC":
            cl = "Cloudy"

    print(f"Skies: {cl}")

    ws = weather_data['windSpeed']['value']
    if ws is None:
        ws = "N/A"
    else:
        ws = weather_data['windSpeed']['value'] * 0.621
        ws = f"{round(ws, 1)} MPH"

    wd = weather_data['windDirection']['value']
    if wd is None:
        wd = "N/A"
    else:
        if wd > 337.5 and wd <= 360 or wd >= 0 and wd < 22.5:
            wd = "South"
        elif wd > 22.5 and wd < 67.5:
            wd = "Southwest"
        elif wd > 67.5 and wd < 112.5:
            wd = "West"
        elif wd > 112.5 and wd < 157.5:
            wd = "Northwest"
        elif wd > 157.5 and wd < 202.5:
            wd = "North"
        elif wd > 202.5 and wd < 247.5:
            wd = "Northeast"
        elif wd > 247.5 and wd < 292.5:
            wd = "East"
        elif wd > 292.5 and wd < 337.5:
            wd = "Southeast"

    print(f"Wind: {ws} - {wd}")

    if weather_data['windGust']['value'] is None:
        wg = "N/A"
    else:
        wg = weather_data['windGust']['value'] * 0.621
        wg = f"{round(wg, 1)} MPH"

    print(f"Wind Gusts: {wg}")

    hum = weather_data['relativeHumidity']['value']
    if hum is None:
        hum = "N/A"
    else:
        hum = f"{round(hum, 1)} %"
    print(f"Humidity: {hum}")

    dp = weather_data['dewpoint']['value']
    if dp is None:
        dp = "N/A"
    else:
        dp = (weather_data['dewpoint']['value'] * 9/5) + 32
        dp = f"{round(dp, 1)} F"

    print(f"Dewpoint: {dp}")

    bp = weather_data['barometricPressure']['value']
    if bp is None:
        bp = "N/A"
        pressure = "N/A"
    else:
        bp = (weather_data['barometricPressure']['value'] * 0.0002953)

        if bp < 29.5:
            pressure = "Low"
        elif bp >= 29.5 and bp <= 30.2:
            pressure = "Normal"
        elif bp > 30.2:
            pressure = "High"

        bp = f"{round(bp, 1)} inHg"

    print(f"Pressure: {pressure} - {bp}")


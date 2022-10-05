from prefect import flow, task
import httpx

#fsspec

@task
def fetch_weather(lat, lon):
    base_url = "https://api.open-meteo.com/v1/forecast"
    weather = httpx.get(
        base_url,
        params = dict(latitude = lat, longitude = lon, hourly = "temperature_2m"),
    )
    print(weather)
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    return most_recent_temp


@task
def save_weather(temp):
    with open("weather.csv", "w+") as w:
        w.write(str(temp))
    return "Successfully wrote temp"


@flow
def weather_pipeline(lat,lon):
    temp = fetch_weather(lat,lon)
    result = save_weather(temp)
    print(result)




if __name__ == "__main__":
    weather_pipeline(52.52,13.41)
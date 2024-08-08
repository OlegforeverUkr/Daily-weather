import openmeteo_requests
import os

import requests
import requests_cache
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from retry_requests import retry

load_dotenv(find_dotenv(raise_error_if_not_found=True))

TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')


def get_weather():
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 49.4183,
        "longitude": 26.9794,
        "hourly": ["temperature_2m", "apparent_temperature"],
        "timezone": None,
        "forecast_days": 1
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()

    normal_temp_2m = [round(float(i), 1) for i in hourly_temperature_2m]
    normal_apparent_temperature = [round(float(i), 1) for i in hourly_apparent_temperature]

    hourly_time = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
    hourly_hours_only = hourly_time.strftime("%H:00")

    hourly_data = {
        "Часы": hourly_hours_only,
        "Температура": normal_temp_2m,
        "Ощущается как": normal_apparent_temperature
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    return hourly_dataframe.to_string()



def send_to_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

    params = {
        'chat_id': TELEGRAM_CHANNEL_ID,
        'text': f'Доброе утро!\nПогода на сегодня\n\n{message}'
    }

    res = requests.post(url, params=params)
    res.raise_for_status()

    return res.json()



if __name__ == '__main__':
    weather = get_weather()
    print(weather)
    send_to_telegram(weather)
import openmeteo_requests
import os

import requests
import requests_cache
import pandas as pd
from dotenv import load_dotenv
from retry_requests import retry
from tabulate import tabulate

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')


def get_weather() -> str:
    # Create a cache session with an expiration time of 1 hour
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    # Create a retry session with 5 retries and a backoff factor of 0.2
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    # Create an OpenMeteo client with the retry session
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 49.453551,
        "longitude": 27.014202,
        "hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability"],
        "timezone": None,
        "forecast_days": 1
    }

    # Retrieve the weather forecast
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()

    # Round the temperature values to 1 decimal place
    normal_temp_2m = [round(float(i), 1) for i in hourly_temperature_2m]
    normal_apparent_temperature = [round(float(i), 1) for i in hourly_apparent_temperature]
    normal_precipitation_probability = [round(float(i), 1) for i in hourly_precipitation_probability]

    # Create a date range for the hourly forecast
    hourly_time = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
    hourly_hours_only = hourly_time.strftime("%H:00")

    # Create a DataFrame with the forecast data
    hourly_data = {
        "Time": hourly_hours_only,
        "t°C": normal_temp_2m,
        "Feel like": normal_apparent_temperature,
        "Fallouts %": normal_precipitation_probability
    }
    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Return a tabulate representation of the DataFrame
    return tabulate(hourly_dataframe, headers="keys", tablefmt="plain", numalign="center", stralign="center", showindex=False)



def send_to_telegram(message: str) -> dict:
    # Construct the URL for the Telegram Bot API
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

    # Set the parameters for the request
    params = {
        'chat_id': TELEGRAM_CHANNEL_ID,
        'text': f'Доброе утро!\nПогода на сегодня\n\n```{message}```',
        'parse_mode': 'Markdown'
    }

    # Send the request to the Telegram Bot API
    res = requests.post(url, params=params)

    # Raise an exception if the request fails
    res.raise_for_status()

    # Return the JSON response from the Telegram Bot API
    return res.json()


if __name__ == '__main__':
    weather = get_weather()
    print(weather)
    send_to_telegram(weather)

import requests
import json

from Tools.tools import log

def Get():
    url = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}' \
    .format(lat='49.13449946', lon='2.569664388', appid='32f8b21e3cebf9f06ba83155a946bbb9')
    try:
        res = json.loads(requests.get(url).text)
    except Exception as e:
        log('Error while get temperature', e)
    if not res.get('main'):
        return None
    cleanRes = {
        'temp': round(float(res["main"]["temp"])-273.15, 2),
        'pressure': res['main']['pressure'],
        'humidity': res['main']['humidity'],
        'wind': res['wind']['speed'],
        'meteo': res['weather'][0]['main'],
    }
    return cleanRes;
Get()
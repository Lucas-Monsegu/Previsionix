import requests
import json
import datetime
from .learn import Model
import asyncio

PREVISION = None


def FToD(F):
    return round(float(F-273.15), 2)


async def getXForecast():

    r = requests.get(
        'https://api.openweathermap.org/data/2.5/onecall?lat=49.13449946&lon=2.569664388&exclude=hourly,minutely&appid=32f8b21e3cebf9f06ba83155a946bbb9')
    res = json.loads(r.text)
    X = []
    day = datetime.datetime.today().weekday()
    l = []
    for i in range(8):
        day = (day + 1) % 7
        month = (datetime.datetime.today() + datetime.timedelta(days=i)).month
        li = []
        if i > 0:
            li = [day, month, FToD(res['daily'][i-1]['temp']['day']),
                  res['daily'][i-1]['wind_speed'], res['daily'][i-1]['humidity']]
            X.append(li)
        else:
            # li = [day, month, FToD(res['current'][i-1]['temp']['day']),
            #       res['wind_speed'], res['humidity']]
            pass
        l.append(day)
    return X, l


async def predict():
    print('predict')
    global PREVISION
    week, days = await getXForecast()
    PREVISION = json.dumps(
        list(zip(map(round, Model.SVR.predict(week)), days)))
    print(PREVISION)

import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import motor.motor_asyncio
import asyncio
import datetime
import requests
import json


client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.previsionix


def __months(start_month, start_year, end_month, end_year):
    return ((str(m_y // 12).zfill(2), str((m_y % 12) + 1).zfill(2)) for m_y in
            reversed(range(12 * start_year + start_month - 1, 12 * end_year + end_month)))


def FToD(F):
    return round(float(F-273.15), 2)


def getXForecast():
    r = requests.get(
        'https://api.openweathermap.org/data/2.5/onecall?lat=49.13449946&lon=2.569664388&exclude=hourly,minutely&appid=32f8b21e3cebf9f06ba83155a946bbb9')
    res = json.loads(r.text)
    X = []
    day = datetime.datetime.today().weekday()
    for i in range(8):
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
        day = (day + 1) % 7

    return X


async def fetchData():
    X = []
    Y = []
    for month in __months(1, 2018, 9, 2020):
        print(f'all-{month[0]}-{month[1]}DelayDaily')
        cursor = db[f'all{month[0]}-{month[1]}DelayDaily'].find()
        for doc in await cursor.to_list(length=100):
            doc['month'] = month[1]
            doc['year'] = month[0]
            doc['day'] = doc['_id'].generation_time.weekday()
            li = [doc['day'], doc['month'], doc['temperature'],
                  doc['wind'], doc['humidity']]
            X.append(li)
            Y.append(doc['delay'])
    return X, Y

a = asyncio.get_event_loop().run_until_complete(fetchData())
print(a)
X = a[0]
y = a[1]
print(len(X), len(y))
indexes = list(range(len(X)))
i_rand = np.random.shuffle(indexes)

x_learn, x_validate, y_learn, y_validate = [], [], [], []

for i in indexes[0:int(len(X)*0.75)]:
    x_learn.append(X[i])
    y_learn.append(y[i])
for i in indexes[int(len(X)*0.25):]:
    x_validate.append(X[i])
    y_validate.append(y[i])

svr = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)

svr.fit(x_learn, y_learn)
print('score', svr.score(x_validate, y_validate))
week = getXForecast()
print(svr.predict(week))

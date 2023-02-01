import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import motor.motor_asyncio
import asyncio
import datetime
import requests
import json


class Model:
    SVR = None


SVRMODEL = None


async def sleepAndDo(s, func):
    print('sleep learn', s)
    await asyncio.sleep(s)
    func()


async def Learn():
    client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    db = client.previsionix
    global SVRMODEL

    a = await fetchData(db)
    X = a[0]
    y = a[1]
    print(len(X), len(y))
    indexes = list(range(len(X)))
    i_rand = np.random.shuffle(indexes)

    x_learn, x_validate, y_learn, y_validate = [], [], [], []

    for i in indexes[0:int(len(X)*0.90)]:
        x_learn.append(X[i])
        y_learn.append(y[i])
    for i in indexes[int(len(X)*0.10):]:
        x_validate.append(X[i])
        y_validate.append(y[i])

    svr = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)

    svr.fit(x_learn, y_learn)
    Model.SVR = svr
    print('score', svr.score(x_validate, y_validate))
    print(Model.SVR)


def __months(start_month, start_year, end_month, end_year):
    return ((str(m_y // 12).zfill(2), str((m_y % 12) + 1).zfill(2)) for m_y in
            reversed(range(12 * start_year + start_month - 1, 12 * end_year + end_month)))


def FToD(F):
    return round(float(F-273.15), 2)


async def fetchData(db):
    X = []
    Y = []
    w = []
    for month in __months(1, 2018, 9, 2020):
        print(f'all-{month[0]}-{month[1]}DelayDaily')
        cursor = db[f'all{month[0]}-{month[1]}DelayDaily'].find()
        for doc in await cursor.to_list(length=100):
            w.append(doc['delay'])
            doc['month'] = month[1]
            doc['year'] = month[0]
            doc['day'] = doc['_id'].generation_time.weekday()
            li = [doc['day'], doc['month'], doc['temperature'],
                  doc['wind'], doc['humidity']]
            X.append(li)
            Y.append(doc['delay'])
    w.sort()
    third = len(w)//3
    print('tier1', w[third], 'tier2', w[2*third])
    print(w[-1])
    print('average', sum(w)/len(w))
    return X, Y

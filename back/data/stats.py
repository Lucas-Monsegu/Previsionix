import motor.motor_asyncio
import pymongo
import redis
from datetime import datetime
import json

red = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.previsionix


def __months(start_month, start_year, end_month, end_year):
    return ((str(m_y // 12).zfill(2), str((m_y % 12) + 1).zfill(2)) for m_y in
            reversed(range(12 * start_year + start_month - 1, 12 * end_year + end_month)))


async def Delay(attraction):
    collection = db[attraction + 'DelayStats']
    return await collection.find_one()


async def Humidity(attraction):
    collection = db[attraction + 'HumidityStats']
    return await collection.find_one()


async def Temperature(attraction):
    collection = db[attraction + 'TemperatureStats']
    return await collection.find_one()


async def Wind(attraction):
    collection = db[attraction + 'WindStats']
    return await collection.find_one()


async def TodayHourAll():
    collection = db["allDelayHourly"]
    res = collection.find().sort("hour", pymongo.ASCENDING)
    res = [(int(i['delay']), i['_id']) async for i in res]
    r = [i[0] for i in res]
    t = '~~' if len(r) == 0 else res[-1][1].generation_time.timestamp()
    return {'values': r, 'timestamp': t}


async def lastTemperature():
    temp = red.get('PXRecentTemperature')
    if temp is None:
        return json.dumps({'value': '~~', 'timestamp': '~~'})
    return temp


async def worthAttr():
    attr = red.get('PXWorthAttr')
    if attr == None:
        return json.dumps({'value': '~~', 'timestamp': '~~'})
    return attr


async def monthDelays(attraction, month):
    date = None
    try:
        date = datetime.strptime(month, '%Y-%m')
    except:
        return {'value': '~~', 'timestamp': '~~'}
    collection = db[attraction + date.strftime('%Y-%m') + 'DelayDaily']
    cursor = collection.find({})
    res = {d['_id'].generation_time.strftime(
        '%Y-%m-%d'): int(d['delay']) async for d in cursor}
    return res


async def allDelays(attraction):
    now = datetime.now()
    res = {}
    for month in __months(now.month, now.year - 1, now.month, now.year):  # remove now.month -1
        collection = db[attraction + '-'.join(month) + 'DelayDaily']
        cursor = collection.find({})
        async for d in cursor:
            res[d['_id'].generation_time.strftime(
                '%Y-%m-%d')] = int(d['delay'])
    return res


async def AllStats():
    now = datetime.now()
    res = {}
    for month in __months(now.month, now.year - 1, now.month, now.year):  # remove now.month-1
        collection = db['all' + '-'.join(month) + 'DelayDaily']
        cursor = collection.find({})
        async for d in cursor:
            res[d['_id'].generation_time.strftime(
                '%Y-%m-%d')] = [int(d['temperature']), d['humidity'], d['wind'], d['delay']]
    return res

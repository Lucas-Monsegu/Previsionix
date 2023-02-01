import asyncio
import asterix
import temperature
import logging
from pymongo import MongoClient
from Tools.tools import log
import datetime
import json
import operator
import math
import schedule
import time
import redis

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
f = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(f)
logger.addHandler(sh)
red = redis.Redis(host='localhost', port=6379, db=0)


client = MongoClient('localhost', 27017)
db = client.previsionix

def cleanDB():
    for attr in ['AttentionMenhir', 'PegaseExpress', 'Discobelix', 'LeDefideCesar', 'LesEspionsdeCesar', 'SOSNumerobis', 
                'RomusetRapidus', 'OzIris', 'LaTraceduHourra', 'Goudurix', 'EpidemaisCroisiere', 'LesChaisesVolantes', 
                'LaGalere', 'LeChevaldeTroie', 'MenhirExpress', 'LesChaudrons', 'LOxygenarium', 'LHydredeLerne',
                'LeVoldIcare', 'TonnerredeZeus', 'all']:
        collection = db[attr+'DelayHourly']
        if collection.count() != 0:
            log('had to clean', attr+'DelayHourly')
        collection.drop()

    collection = db.lastHourWeather
    if collection.count() != 0:
        log('had to clean', 'lastHourWeather')
    collection.drop()
  
    collection = db.lastHourDelay
    if collection.count() != 0:
        log('had to clean', 'lastHourDelay')
    collection.drop()



def getAverages(datas):
    tab = {key: [0, 0] for key in datas[0] if key != '_id'}
    for data in datas:
        for key in data:
            if key == '_id':
                continue
            a = 0
            try:
                a = float(data[key])
            except:
                if tab.get(key) and tab[key][1] == 0:
                    del tab[key]
                continue
            if tab.get(key) != None:
                tab[key][1] += 1
                tab[key][0] += a
    return {key: tab[key][0]/tab[key][1] for key in tab}


def Daily():
    collection = db.allDelayHourly
    if collection == None or collection.count() == 0:
        log('no data in daily')
        return
    for attr in ['AttentionMenhir', 'PegaseExpress', 'Discobelix', 'LeDefideCesar', 'LesEspionsdeCesar', 'SOSNumerobis', 
                'RomusetRapidus', 'OzIris', 'LaTraceduHourra', 'Goudurix', 'EpidemaisCroisiere', 'LesChaisesVolantes', 
                'LaGalere', 'LeChevaldeTroie', 'MenhirExpress', 'LesChaudrons', 'LOxygenarium', 'LHydredeLerne',
                'LeVoldIcare', 'TonnerredeZeus']:
        collection = db[attr+'DelayHourly']
        if collection.count() == 0:
            continue
        datas = [d for d in collection.find({}).sort('timestamp', -1)]
        collection.drop()
        averages = getAverages(datas)
        collection = db[attr+datetime.datetime.now().strftime('%Y-%m')+'DelayDaily']
        collection.insert_one({'delay': averages['delay']})

    attr = 'all'
    collection = db[attr+'DelayHourly']
    datas = [d for d in collection.find({}).sort('timestamp', -1)]
    collection.drop()
    averages = getAverages(datas)
    collection = db['weatherHourly']    
    if collection.count() == 0:
        log('CRITIC: do not have weather Hourly, THERE IS A PROBLEM WITH OPENWEATHER MAP')    
    averagesWeather = getAverages([d for d in collection.find({})])
    collection.drop()
    collection = db[attr+datetime.datetime.now().strftime('%Y-%m')+'DelayDaily']
    collection.insert_one({'delay':averages['delay'], 'temperature': averagesWeather['temperature'], 'wind':averagesWeather['wind'], 'humidity': averagesWeather['humidity']})
    

    
def Hourly():

    hour = datetime.datetime.now().hour
    print(hour)
    if not 10 <= hour <= 18 or not IsOpenedToday():
        print('passing', hour)
        return
    def delays():

        def GetClosed(datas):
            tab = {}
            for data in datas:
                for key in data:
                    if key == '_id':
                        continue
                    if data[key] == 'FERME' or data[key] == 'INDISPONIBLE':
                        tab[key] = 1
            return tab
        collection = db.lastHourDelay
        datas = [d for d in collection.find({}).sort('timestamp', -1)]
        collection.drop()
        if not datas:
            return None
        hourAverage = getAverages(datas)
        closed = GetClosed(datas)
        # Add average
        totalHourAverage = sum(hourAverage.values()) / len(hourAverage.values())
        for attr in hourAverage.keys():
            collection = db[attr+"DelayHourly"]
            collection.insert_one({'delay': hourAverage[attr], 'hour': hour})
            collection = db[attr + "DelayStats"]
            collection.find_one_and_update({"hour": hour}, {"$inc": {"average.v": hourAverage[attr], 'average.c': 1}}, upsert=True)
        for attr in closed.keys():
            collection = db[attr + 'ClosedStats']
            collection.find_one_and_update({"hour": hour}, {"$inc": {"value": 1}}, upsert=True)            
        collection = db['allDelayStats']
        collection.find_one_and_update({"hour": hour}, {"$inc": {"average.v": totalHourAverage, "average.c": 1}}, upsert=True)
        collection = db['allDelayHourly']
        collection.insert_one({'delay': totalHourAverage, 'hour': hour})

        return hourAverage

    def weather(hourAverage):

        def formatTemperature(data):
            temp = data['temperature']
            return min(((abs(i-temp),i) for i in range(-5, 45, 5)),key=operator.itemgetter(0))[1]

        def formatWind(data):
            wind = data['wind']
            return min(((abs(i-wind),i) for i in range(0, 20, 2)),key=operator.itemgetter(0))[1]

        def formatHumidity(data):
            humidity = data['humidity']
            return min(((abs(i-humidity),i) for i in range(0, 100, 10)),key=operator.itemgetter(0))[1]

        def getFormated(data, t):
            if t == 'temperature':
                return formatTemperature(data)
            elif t == 'wind':
                return formatWind(data)
            else:
                return formatHumidity(data)
        
        collection = db.lastHourWeather
        datas = [d for d in collection.find({}).sort('timestamp', -1)]
        collection.drop()
        if not datas:
            log('no weather data in hourly')
            return
        averages = getAverages(datas)
        print(averages)
        collection = db['weatherHourly']
        collection.insert_one({'hour': hour, 'temperature': averages['temperature'], 'wind': averages['wind'],
        'humidity': averages['humidity']})
        if not hourAverage:
            log('no delay data in hourAverage')
            return
        for mode in ['temperature', 'wind', 'humidity']:
            averages[mode] = getFormated(averages, mode)
        totalHourAverage = sum(hourAverage.values()) / len(hourAverage.values())
        for mode in ['temperature', 'wind', 'humidity']:
            for attr in hourAverage.keys():
                collection = db[attr+mode.title()+'Stats']
                val = averages[mode]
                collection.find_one_and_update({mode: val}, {"$inc": {"average.v": hourAverage[attr], 'average.c': 1}}, upsert=True)
        
        for mode in ['temperature', 'wind', 'humidity']:
            collection = db['all'+mode.title()+'Stats']
            val = averages[mode]
            collection.find_one_and_update({mode: val}, {"$inc": {"average.v": totalHourAverage, 'average.c': 1}}, upsert=True)

    d = delays()
    weather(d)
def Minutly():

    def getMostWorthAttr(datas, hour):
        m = [math.inf, 'Any']
        for attr in datas:
            currentLatency = datas[attr]
            collection = db[attr + 'DelayStats']
            averageLatency = collection.find_one({'hour': hour})
            difference = 0
            if averageLatency == None or not currentLatency.isnumeric():
                difference = math.inf
            else:
                difference = float(currentLatency) - float(averageLatency['average']['v']) 
            if difference < m[0]:
                print(difference, attr)
                m[0] = difference
                m[1] = attr
        return m[1]

    hour = datetime.datetime.now().hour

    try:
        tempRes = temperature.Get()
        if tempRes == None:
            log('cannot get temperature', tempRes)
            return
        red.set('PXRecentTemperature', json.dumps({'value': tempRes['temp'], 'timestamp': datetime.datetime.now().timestamp()}))
        if not 10 <= hour <= 18: 
            print('passing', hour)
            return  
        if not IsOpenedToday():
            print('closed')
            return        
        asterixRes = asterix.Get()
        if asterix == None:
            log('cannot get asterix', asterixRes)
            return
        
        collection = db.lastHourDelay
        datas = {attr: asterixRes[attr] for attr in asterixRes.keys()}
        collection.insert_one(datas)
        collection = db.lastHourWeather
        data={}
        data['temperature'] = tempRes['temp']
        data['humidity'] = tempRes['humidity']
        data['wind'] = tempRes['wind']
        collection.insert_one(data)
        worthattr = getMostWorthAttr(datas,hour)
        red.set('PXWorthAttr', json.dumps({'value': worthattr, 'timestamp': datetime.datetime.now().timestamp()}))
    except Exception as e:
        logger.error('Error while connecting to APIS'+str(e))

def IsOpenedToday():
    todayOpened = asterix.IsOpened()
    log('TODAY IS OPEN' if todayOpened else 'TODAY IS CLOSED')
    return todayOpened
#Minutly()
#Hourly()
#Daily()
if __name__ == "__main__":    
    schedule.every().day.at('10:01').do(IsOpenedToday)
    schedule.every(4).to(5).minutes.do(Minutly)
    schedule.every().hour.at(':59').do(Hourly)
    schedule.every().day.at('23:00').do(Daily)
    schedule.every().day.at('05:00').do(cleanDB)
    log('Worker UP and running')
    log('TODAY IS OPEN' if IsOpenedToday() else 'TODAY IS CLOSED')
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            log('error in main loop', str(e))
        time.sleep(1)

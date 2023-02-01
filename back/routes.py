from aiohttp import web
import data.stats
import prevision.predict
import random
import json
import time
routes = web.RouteTableDef()


@routes.get('/')
async def hello_world(request):
    time.sleep(1)
    return web.Response(text=json.dumps(([random.randint(0, 30,) for _ in range(11)])))


@routes.get('/api/prediction')
async def predict(request):
    print('called prediction')
    return web.Response(text=prevision.predict.PREVISION)


@routes.get('/api/todayHourAll')
async def todayHour(request):
    return web.Response(text=json.dumps(await data.stats.TodayHourAll()))


@routes.get('/api/lastTemperature')
async def lastTemperature(request):
    return web.Response(text=await data.stats.lastTemperature())


@routes.get('/api/worthAttraction')
async def worthAttraction(request):
    return web.Response(text=await data.stats.worthAttr())


@routes.get('/api/month-delay/{attraction}/{date}')
async def getMonthDelays(request):
    return web.Response(text=json.dumps(await data.stats.monthDelays(request.match_info['attraction'], request.match_info['date'])))


@routes.get('/api/all-daily-infos')
async def getAllDailyInfos(request):
    return web.Response(text=json.dumps(await data.stats.AllStats()))


@routes.get('/api/all-daily-delays/{attraction}')
async def getDailyDelays(request):
    return web.Response(text=json.dumps(await data.stats.allDelays(request.match_info['attraction'])))

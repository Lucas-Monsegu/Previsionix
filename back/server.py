import aiohttp
import asyncio
from routes import routes
from prevision.learn import Learn
from prevision.predict import predict
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

loop = asyncio.get_event_loop()

logging.basicConfig(level=logging.DEBUG)
app = aiohttp.web.Application()
app.router.add_routes(routes)


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(Learn, 'interval', seconds=60*60*24*30)
    scheduler.add_job(predict, 'interval', seconds=60*60*24)
    a = scheduler.start()
    await Learn()
    await predict()
    await aiohttp.web._run_app(app, port=5000),
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, 'localhost', 5000)
    await site.start()

loop.run_until_complete(main())

import requests
import sys
import aiohttp
import asyncio
import time
from urllib3 import Timeout, PoolManager

class server_data:
    """
        Get data from web server
        - Live data is got anynchronously from three endpoints for sun, price and demand data
        - Deferables and History data is run with 2 separate functions
    """
    def __init__(self) -> None:
        self.url = 'https://icelec50015.azurewebsites.net'
        self.get_url = lambda endpoint : self.url+endpoint

        self.live_urls = list(map(self.get_url,['/sun', '/price', '/demand']))
        self.session = None
        self.json = ""
        self.headers = {'Accept-Encoding':'gzip'}
        self.other_pools = {u:PoolManager(timeout=Timeout(connect=0.5, read=3)) for u in map(self.get_url, ['/deferables', '/yesterday'])}
        self.cache = {'buy_price':0, 'demand':0, 'sell_price':0, 'sun':0, 'deferables':0}
        self.event_loop = asyncio.get_event_loop()

        self.data_points = 60
        self.parsed_data = {'buy_price':[], 'demand':[], 'sell_price':[], 'sun':[], 'deferables':[]}
        self.tick = 0

        # fill cache with most recent history in case live data fails on first call
        self.init_cache_and_history()

    def starting_tick(self):
        self.live_data(True)  # call this just to get live tick

        start = self.tick
        print(start)

        while(self.tick != start):
            self.live_data()

        return self.tick

    def init_cache_and_history(self):
        self.set_historical_prices()

        for k, v in self.parsed_data.items():
            self.cache[k] = v[-1] if v else 0

    async def fetch(self, url):
        async with self.session.get(url, headers=self.headers) as response:
            return await response.json()
            
    async def fetch_multiple(self, urls):
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks)
    
    async def create_session(self):
        if(not self.session or self.session.closed):
            timeout = aiohttp.ClientTimeout(total=1)
            self.session = aiohttp.ClientSession(timeout=timeout)

    async def close_session(self):
        if(self.session):
            await self.session.close()
    
    async def get_live(self, tick=False):
        await self.create_session()

        try:
            responses = await self.fetch_multiple(self.live_urls)
            self.tick = responses[-1]["tick"]

            if(not tick):
                for r in responses:
                    if("sun" in r):
                        self.parsed_data['sun'] = r["sun"]
                    elif("buy_price" in r):
                        self.parsed_data['buy_price'] = r["buy_price"]
                        self.parsed_data['sell_price'] = r["sell_price"]
                    else:
                        self.parsed_data['demand'] = r["demand"]

                self.cache = self.parsed_data

        except aiohttp.ClientError as e:
            print(f"CLient Error: {e}, Using cache")
            self.tick += 1
            self.parsed_data = self.cache
        
        except asyncio.TimeoutError as e:
            print(f"Timeout Error: {e}, Using cache")
            self.tick += 1
            self.parsed_data = self.cache

        finally:
            await self.close_session()

    def live_data(self, tick=False):
        return self.event_loop.run_until_complete(self.get_live(tick))

    def set_historical_prices(self):
        url = self.get_url('/yesterday')
        http = self.other_pools[url]
        response = http.request('GET', url, headers=self.headers)

        self.json = response.json()

        for s in ['buy_price', 'demand', 'sell_price']:
            self.parsed_data[s] = [self.json[i][s] for i in range(self.data_points)]
    
    def deferables(self):
        url = self.get_url('/deferables')
        http = self.other_pools[url]
        response = http.request('GET', url, headers=self.headers)

        self.json = response.json()

        self.parsed_data['deferables'] = self.json  
        
if (__name__ == "__main__"):
    serve = server_data()

    while True:
        time.sleep(5)
        serve.live_data()

        print(serve.parsed_data, " ", serve.tick)
 
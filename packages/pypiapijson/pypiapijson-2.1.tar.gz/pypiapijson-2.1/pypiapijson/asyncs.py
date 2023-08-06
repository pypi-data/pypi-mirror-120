import aiohttp
from typing import Optional
async def getter(url,headers=False):
	async with aiohttp.ClientSession() as session:
		if headers:
			async with session.get(url,headers={"Content-type":"application/json","Accept":"application/json"}) as response:
				return await response
		async with session.get(url) as response:
			return await response
async def get(name):
	"""Get the information about package with that name provided if that was not exist or pypi api down then say error"""
	thing = await getter(url=f"https://pypi.org/pypi/{name}/json")
	return await thing.json() if thing.status == 200 else None
async def getbyv(name,ver:Optional[str,int]):
	"""Get the information about package with that name provided if that was not exist or pypi api down then say error"""
	thing = await getter(url=f"https://pypi.com/pypi/{name}/{ver}/json")
	return await thing.json() if thing.status == 200 else None

async def status():
	thing = await getter(url="https://pypi.org/stats",headers=True)
	return await thing.json() if thing.status == 200 else None
def helpme():
	print("Hello!\nUsage:\nget(packagename : string)\nGet information the paclage name that you provided and get the information in lastest version if there\'s no package it\'ll return none and raise error\ngetbyv(packagename : string,version : float or string) Do everything like get but you\'ll need to specify version the package have if there\'s wrong return None and raise error\nstatus()This will retrieve what package take most space and this fucntion is asynchronous function so run it with asyncio or await it.")
global listfunc
listfunc = ["get","getbyv","status"]
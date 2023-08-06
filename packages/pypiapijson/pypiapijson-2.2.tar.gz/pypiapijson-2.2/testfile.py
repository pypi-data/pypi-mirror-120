import pypiapijson as  __init__;print(__init__.get("flask"));print(__init__.getbyv("pypiapijson",1));print(__init__.status())
asyncs = __init__.asyncs
async def test():print(asyncs.get("flask"))
import asyncio;print(asyncio.run(test()))
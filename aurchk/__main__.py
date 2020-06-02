import aiohttp
import asyncio

from aurchk.checker import checker
from aurchk.cfgLoad import cfgLoad

# Fetch package info from AUR, and return the dictionary converted from json.
async def fetch(session, pkgname):
    async with session.get("https://aur.archlinux.org/rpc/?v=5&type=info&arg[]=" + pkgname) as response:
        return await response.json()

async def main():
    # Check package update with coroutines.
    pkgListPath, pkgClonePath, oldVerDict = await cfgLoad()

    chk = checker(pkgListPath, pkgClonePath, oldVerDict)
    
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[chk.chkVer(pkgname, await fetch(session, pkgname)) for pkgname in oldVerDict])

    print('New versions available for these packages:')
    await asyncio.gather(*[chk.postChk(pkgname) for pkgname in oldVerDict])
    
# Create the asyncio loop and run main().
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

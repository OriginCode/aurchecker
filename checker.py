#!/usr/bin/env python3.8
import aiohttp
import asyncio
import pyalpm
import json
import git
import argparse
from pathlib import Path

# Parse arguments from command line stdin.
argParser = argparse.ArgumentParser(description='Check AUR update.')
argParser.add_argument('-c', '--config', type=str, help='Manually set the path to the config file.', nargs='?')
args = argParser.parse_args()

# Fetch package info from AUR, and return the dictionary converted from json.
async def fetch(session, pkgname):
    async with session.get("https://aur.archlinux.org/rpc/?v=5&type=info&arg[]=" + pkgname) as response:
        return await response.json()

async def main():
    # Parse config files, allow using the argument given.
    if args.config != None:
        cfgPath = Path(args.config)
        if not cfgPath.exists():
            print('No such config file.')
            exit(1)
    else:
        cfgPath = Path.home().joinpath(Path('.config/aurchk/config.json'))

    cfgParentPath = cfgPath.parents[0]
    
    if cfgPath.exists() and cfgPath.stat().st_size > 0:
        with open(cfgPath) as f:
            config = json.load(f)
    else:
        if not cfgParentPath.exists():
            Path.home().joinpath(Path('.config/aurchk/')).mkdir(parents=True)
        else:
            cfgPath.touch()

        with open(cfgPath, 'w') as f:
            # Default config, if the default config file (path) does not exist, create one include the default config.
            config = {
                    'pkgListPath': str(Path.home().joinpath(Path('.config/aurchk/pkgs.json'))),
                    'pkgClonePath': str(Path.home().joinpath(Path('.cache/aurchk/')))
                    }
            f.write(json.dumps(config, indent=4))
    
    # Another config file for storing package names and their current versions. **MUST EXIST**
    if (pkgListPath := Path(config['pkgListPath'])).exists():
        with open(pkgListPath) as f:
            oldVerDict = json.load(f)
    else:
        print('Package list file not found! (Default: ${HOME}/.config/aurchk/pkgs.json)')
        exit(1)

    if not (pkgClonePath := Path(config['pkgClonePath'])).exists():
        pkgClonePath.mkdir(parents=True)
    
    # End of config loading.

    # Version checking.
    # Variables that store new versions fetched from AUR, and result of version comparison from chkVer().
    newVerDict = {}
    chkResult = {}
    
    # Use vercmp from pyalpm to compare the old version and the new version fetched.
    async def chkVer(pkgname, response):
        try:
            newVer = response['results'][0]['Version']
        except:
            newVer = "null"
        newVerDict[pkgname] = newVer
        chkResult[pkgname] = (pyalpm.vercmp(newVer, oldVerDict[pkgname]) == 1)
    
    # After chkVer, if the package has a new version, show the result and clone the repo into the pkgClonePath given in the config.
    async def postChk(pkgname):
        if chkResult[pkgname]:
            print(pkgname + ': '+ oldVerDict[pkgname] + ' => ' + newVerDict[pkgname])
            git.Git(pkgClonePath).clone("https://aur.archlinux.org/{pkgname}.git".format(pkgname=pkgname))
            print("Cloned the repo of " + pkgname)
            with open(pkgListPath, 'w') as f:
                f.write(json.dumps(newVerDict, indent=4))
    
    # Check package update with coroutines.
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[chkVer(pkgname, await fetch(session, pkgname)) for pkgname in oldVerDict])

    print('New versions available for these packages:')
    await asyncio.gather(*[postChk(pkgname) for pkgname in oldVerDict])
    
# Create the asyncio loop and run main().
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

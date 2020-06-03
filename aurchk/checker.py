import json
import pyalpm
import asyncio
from pathlib import Path
from git.cmd import Git
from termcolor import colored

# Use vercmp from pyalpm to compare the old version and the new version fetched.
class checker():
    def __init__(self, pkgListPath, pkgClonePath, oldVerDict):
        self.newVerDict = {}
        self.chkResult = {}
        self.pkgListPath = pkgListPath
        self.pkgClonePath = pkgClonePath
        self.oldVerDict = oldVerDict

    # Version checking.
    # Variables that store new versions fetched from AUR, and result of version comparison from chkVer().
    async def chkVer(self, pkgname, response):
        try:
            newVer = response['results'][0]['Version']
        except:
            newVer = "null"
        self.newVerDict[pkgname] = newVer
        self.chkResult[pkgname] = (pyalpm.vercmp(newVer, self.oldVerDict[pkgname]) == 1)
    
    # After chkVer, if the package has a new version, show the result and clone the repo into the pkgClonePath given in the config.
    async def postChk(self, pkgname):
        if self.chkResult[pkgname]:
            print(pkgname + ': ' + colored(self.oldVerDict[pkgname], 'red', attrs=['bold']) + colored(' => ', 'white', attrs=['bold']) + colored(self.newVerDict[pkgname], 'green', attrs=['bold']))
            
            if (pkgPath := self.pkgClonePath.joinpath(pkgname)).exists():
                Git(pkgPath).pull()
                print(colored('Updated the repo of ', 'green') + pkgname)
            else:
                Git(self.pkgClonePath).clone("https://aur.archlinux.org/{pkgname}.git".format(pkgname=pkgname))
                print(colored('Cloned the repo of ', 'cyan') + pkgname)

            with open(self.pkgListPath, 'w') as f:
                f.write(json.dumps(self.newVerDict, indent=4))
        else:
            print(pkgname + ': ' + colored('Up to date!', 'green', attrs=['bold']) + colored('(' + self.oldVerDict[pkgname] + ')', 'grey', attrs=['dark', 'bold']))
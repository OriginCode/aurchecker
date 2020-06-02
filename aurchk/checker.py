import json
import git
import pyalpm
import asyncio
from pathlib import Path

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
            print(pkgname + ': '+ self.oldVerDict[pkgname] + ' => ' + self.newVerDict[pkgname])
            git.Git(self.pkgClonePath).clone("https://aur.archlinux.org/{pkgname}.git".format(pkgname=pkgname))
            print("Cloned the repo of " + pkgname)
            with open(self.pkgListPath, 'w') as f:
                f.write(json.dumps(self.newVerDict, indent=4))
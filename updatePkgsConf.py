import json
import subprocess
from pathlib import Path

cfgPath = Path.home().joinpath('.config/aurchk/pkgs.json')

if not cfgPath.exists():
    cfgPath.touch()
elif cfgPath.stat().st_size > 0:
    cfgPath.unlink()
    cfgPath.touch()

pmResult = subprocess.Popen(['pacman -Qm'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode().split('\n')[:-1]

pkgsWithVer = {}

for result in pmResult:
    pkg, ver = result.split(' ')
    pkgsWithVer[pkg] = ver

with open(cfgPath, 'w') as f:
    f.write(json.dumps(pkgsWithVer, indent=4))
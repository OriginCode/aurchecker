import json
import asyncio
from pathlib import Path

# Parse config files, allow using the argument given.
async def cfgLoad(args):
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
    
    return pkgListPath, pkgClonePath, oldVerDict
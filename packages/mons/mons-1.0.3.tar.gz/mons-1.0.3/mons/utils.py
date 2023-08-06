import os
import configparser
import json

import hashlib
import zipfile
import shutil

import urllib.request

from click import echo

import dnfile # https://github.com/malwarefrank/dnfile
from dnfile.mdtable import AssemblyRefRow
from pefile import DIRECTORY_ENTRY # https://github.com/erocarrera/pefile

from .config import *

from typing import Union, List, Dict, Any, cast

VANILLA_HASH = {
    'f1c4967fa8f1f113858327590e274b69': ('1.4.0.0', 'FNA'),
    '107cd146973f2c5ec9fb0b4f81c1588a': ('1.4.0.0', 'XNA'),
}

def fileExistsInFolder(path: str, filename: str, forceName=True, log=False) -> Union[str,None]:
    installPath = None
    if os.path.isfile(path):
        if not forceName or os.path.basename(path) == filename:
            installPath = path
        elif log:
            echo(f'error: file `{installPath}` must be called {filename}')
    elif os.path.isdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            installPath = os.path.join(path, filename)
        elif log:
            echo(f'error: {filename} file could not be found in `{installPath}`')
    elif log:
        echo(f'error: `{path}` could not be resolved')
    return installPath

def getMD5Hash(path: str) -> str:
    with open(path, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read(8129)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8129)
    return file_hash.hexdigest()

def unpack(zip: zipfile.ZipFile, root: str, prefix=''):
    totalSize = 0
    for zipinfo in zip.infolist():
        if not prefix or zipinfo.filename.startswith(prefix):
            totalSize += zipinfo.file_size

    progress = 0
    for zipinfo in zip.infolist():
        if not prefix or zipinfo.filename.startswith(prefix):
            zip.extract(zipinfo, root)
            progress += zipinfo.file_size
            printProgressBar(progress, totalSize, 'extracting:')

# shutils.copytree(dirs_exist_ok) replacement https://stackoverflow.com/a/15824216
def copy_recursive_force(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                copy_recursive_force(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        shutil.copyfile(src, dest)

def isUnchanged(src, dest, file):
    srcFile = os.path.join(src, file)
    destFile = os.path.join(dest, file)
    if os.path.exists(destFile):
        return os.stat(destFile).st_mtime - os.stat(srcFile).st_mtime >= 0
    return False

# Print iterations progress - https://stackoverflow.com/a/34325723
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '/', printEnd = "\r", persist=True):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    output = f'\r{prefix} |{bar}| {percent}% {suffix}'
    print(output, end = printEnd)
    # Print New Line on Complete
    if persist and iteration == total: 
        echo()
    elif not persist and iteration == total:
        print('\r' + (' ' * len(output)), end='\r')


def getCelesteVersion(path, hash=None):
    hash = hash or getMD5Hash(path)
    version = VANILLA_HASH.get(hash, '')
    if version:
        return version, True

    orig_path = os.path.join(os.path.dirname(path), 'orig', 'Celeste.exe')
    if os.path.isfile(orig_path):
        hash = getMD5Hash(orig_path)
        version = VANILLA_HASH.get(hash, '')
        if version:
            return version, False

    return None, False

def parseExeInfo(path):
    print('loading exe...', end='\r')
    pe = dnfile.dnPE(path, fast_load=True)
    pe.parse_data_directories(directories=DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR'])
    stringHeap: dnfile.stream.StringsHeap = pe.net.metadata.streams_list[1]

    hasEverest = False
    everestBuild = None

    heapSize = stringHeap.sizeof()
    i = 0
    while i < len(stringHeap.__data__):
        string = stringHeap.get(i)
        if string is None:
            break
        if string == 'EverestModule':
            hasEverest = True
        if str(string).startswith('EverestBuild'):
            everestBuild = string[len('EverestBuild'):]
            hasEverest = True
            break
        i += max(len(string), 1)
        printProgressBar(i, heapSize, 'scanning exe:', persist=False)

    assemRef = pe.net.mdtables.AssemblyRef
    framework = 'FNA' if any(cast(AssemblyRefRow, row).Name == 'FNA' for row in assemRef.rows) else 'XNA'

    return hasEverest, everestBuild, framework

def getInstallInfo(userInfo, install) -> Union[Dict[str, Any], configparser.SectionProxy]:
    path = userInfo.installs[install]['Path']
    mainHash = getMD5Hash(path)
    if userInfo.cache.has_section(install) and userInfo.cache[install].get('Hash', '') == mainHash:
        return userInfo.cache[install]

    if mainHash in VANILLA_HASH:
        version, framework = VANILLA_HASH[mainHash]
        info = {
            'Everest': False,
            'CelesteVersion': version,
            'Framework': framework,
            # EverestBuild: None
        }
    else:
        hasEverest, everestBuild, framework = parseExeInfo(path)
        info = {}
        if hasEverest:
            info['Everest'] = True
            if everestBuild:
                info['EverestBuild'] = everestBuild

            origHash = getMD5Hash(os.path.join(os.path.dirname(path), 'orig', 'Celeste.exe'))
            if origHash in VANILLA_HASH:
                info['CelesteVersion'], _ = VANILLA_HASH[origHash]
        else:
            info['Everest'] = False

        info['Framework'] = framework

    info['Hash'] = mainHash
    userInfo.cache[install] = info.copy() # otherwise it makes all keys in info lowercase
    return info

def buildVersionString(installInfo: Union[Dict[str, Any], configparser.SectionProxy]) -> str:
    versionStr = installInfo.get('CelesteVersion', 'unknown')
    framework = installInfo.get('Framework', None)
    if framework:
        versionStr += f'-{framework.lower()}'
    everestBuild = installInfo.get('EverestBuild', None)
    if everestBuild:
        versionStr += f' + 1.{everestBuild}.0'
    else:
        hasEverest = installInfo.get('Everest', None)
        if hasEverest:
            versionStr += f' + Everest(unknown version)'
    return versionStr

def updateCache(userInfo, install):
    path = userInfo.installs[install]['Path']
    newHash = getMD5Hash(path)

    celesteversion, vanilla = getCelesteVersion(path)
    userInfo.cache[install] = {
        'Hash': newHash,
        'Everest': not vanilla,
    }

    if celesteversion:
        userInfo.cache[install]['CelesteVersion'] = celesteversion
    pass

def parseVersionSpec(string: str) -> int:
    if string.startswith('1.') and string.endswith('.0'):
        string = string[2:-2]
    if string.isdigit():
        buildnumber = int(string)
    else:
        buildnumber = getLatestBuild(string)

    return buildnumber

def getLatestBuild(branch: str) -> int:
    builds = json.loads(urllib.request.urlopen('https://dev.azure.com/EverestAPI/Everest/_apis/build/builds?api-version=6.0').read())['value']
    for build in builds:
        if not (build['status'] == 'completed' and build['result'] == 'succeeded'):
            continue
        if not (build['reason'] == 'manual' or build['reason'] == 'individualCI'):
            continue

        if not branch or branch == build['sourceBranch'].replace('refs/heads/', ''):
            try:
                return int(build['id']) + 700
            except:
                pass
    echo(f'error: `{branch}` branch could not be found')
    return False

def getBuildDownload(build: int, artifactName='olympus-build'):
    return urllib.request.urlopen(f'https://dev.azure.com/EverestAPI/Everest/_apis/build/builds/{build - 700}/artifacts?artifactName={artifactName}&api-version=6.0&%24format=zip')

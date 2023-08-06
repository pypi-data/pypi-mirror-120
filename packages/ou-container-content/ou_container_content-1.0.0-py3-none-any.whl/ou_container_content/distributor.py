"""Distribute files from a source to a target location."""
import json
import math
import os
import shutil

from asyncio import sleep
from hashlib import sha512

from .handlers import send_message


async def precalculate(config: dict) -> None:
    """Precalculate the source file hashes.

    :param config: The configuration with the paths to precalculate
    :type config: dict
    """
    if 'paths' in config:
        for path in config['paths']:
            if os.path.exists(path['source']):
                hashes = await calculate_hashes(path['source'])
                if not os.path.exists(os.path.join(path['source'], '.ou-container-content')):
                    os.makedirs(os.path.join(path['source'], '.ou-container-content'), exist_ok=True)
                with open(os.path.join(path['source'], '.ou-container-content', 'hashes.json'), 'w') as out_f:
                    json.dump(hashes, out_f)


async def distribute(config: dict) -> None:
    """Distribute a full configuration.

    :param config: The configuration with the paths to copy
    :type config: dict
    """
    send_message({
        'message': 'Determining files to update. This can take a bit. Please wait...'
    })
    send_message({
        'component': 'files',
        'state': 'active',
        'progress': 0,
    })
    if 'paths' in config:
        updates = []
        for idx, path in enumerate(config['paths']):
            send_message({
                'component': 'files',
                'state': 'active',
                'progress': math.floor(100 / len(config['paths']) * idx),
            })
            updates.extend(await determine_updates(path))
            await sleep(0.1)
        send_message({
            'message': 'Updating files...'
        })
        for idx, update in enumerate(updates):
            if update[0] == 'dir':
                os.makedirs(update[1], exist_ok=True)
            elif update[0] == 'file':
                dirname = os.path.dirname(update[2])
                os.makedirs(dirname, exist_ok=True)
                shutil.copyfile(update[1], update[2])
            if idx % 10 == 0:
                send_message({
                    'component': 'files',
                    'state': 'active',
                    'progress': math.floor(100 / len(updates) * idx),
                })
                await sleep(0.001)
    send_message({
        'message': 'Your files have been updated.'
    })
    send_message({
        'component': 'files',
        'state': 'complete',
        'progress': 100,
    })


async def determine_updates(path: dict) -> list:
    """Distribute a single path configuration.

    This will copy the file contents from source to target. Depending on the overwrite mode, existing files will or
    will not be overwritten.

    :param path: The path configuration to distribute
    :type path: dict
    """
    updates = []
    if not os.path.exists(os.path.join(path['source'], '.ou-container-content', 'hashes.json')):
        hashes = await calculate_hashes(path['source'])
        if not os.path.exists(os.path.join(path['source'], '.ou-container-content')):
            os.makedirs(os.path.join(path['source'], '.ou-container-content'), exist_ok=True)
        with open(os.path.join(path['source'], '.ou-container-content', 'hashes.json'), 'w') as out_f:
            json.dump(hashes, out_f)
    if os.path.exists(path['source']):
        for basepath, dirnames, filenames in os.walk(path['source']):
            for dirname in dirnames:
                if dirname != '.ou-container-content':
                    targetpath = os.path.join(path['target'],
                                              os.path.join(basepath, dirname)[len(path['source']) + 1:])
                    if not os.path.exists(targetpath):
                        updates.append(('dir', targetpath))
        with open(os.path.join(path['source'], '.ou-container-content', 'hashes.json')) as in_f:
            source_hashes = json.load(in_f)
        target_hashes = await calculate_hashes(path['target'])
        for filepath, hash in source_hashes.items():
            if filepath not in target_hashes:
                updates.append(('file',
                                os.path.join(path['source'], filepath),
                                os.path.join(path['target'], filepath)))
            elif target_hashes[filepath] != hash:
                if path['overwrite'] == 'always':
                    updates.append(('file',
                                    os.path.join(path['source'], filepath),
                                    os.path.join(path['target'], filepath)))
    return updates


async def calculate_hashes(path: str) -> dict:
    """Calculate the hashes for all files in ``path``.

    :param path: The path for which to calculate the hases
    :type path: str
    :return: The calculated hashes
    :retype: dict
    """
    hashes = {}
    for basepath, dirnames, filenames in os.walk(path):
        if '.ou-container-content' not in basepath:
            for filename in filenames:
                filepath = os.path.join(basepath, filename)
                with open(filepath, 'rb') as in_f:
                    hash = sha512(in_f.read())
                hashes[filepath[len(path) + 1:]] = hash.hexdigest()
    return hashes

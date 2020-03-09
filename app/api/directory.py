#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import glob

from app import socketio
from app.api.globals import transmit

DIRECTORY = 'DIRECTORY'


@socketio.on(DIRECTORY)
def directory_handler(data):
    if isinstance(data, str):
        data = json.loads(data)

    if data is None:
        data = {}

    base_path = data.get('base_path', os.path.expanduser("~"))
    new_path = data.get('new_path')
    if new_path is not None:
        base_path = os.path.abspath(os.path.join(base_path, new_path))

    if not os.path.isdir(base_path):
        transmit.errors(DIRECTORY, 'invalid path')
        return

    path = os.path.join(base_path, '*/')
    subdir = []
    for d in glob.glob(path):
        subdir.append(d)

    payload = {
        'base_path': base_path,
        'subdir': subdir,
    }
    transmit.data(DIRECTORY, payload)

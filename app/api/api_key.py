#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from app import socketio
from app.utils import read_config_file, save_config_file
from app.api.globals import transmit, get_dart_fss, cache


DART_API_KEY = 'DART_API_KEY'


def check_authorized():
    api_key = cache.get('DART_API_KEY', None)
    if api_key is None:
        transmit.errors(DART_API_KEY, 'Unauthorized')
        return False
    return True


def set_api_key(api_key):
    try:
        dart = get_dart_fss()
        dart.set_api_key(api_key)
        save_config_file({DART_API_KEY: api_key})
    except ValueError as e:
        api_key = None
        transmit.errors(DART_API_KEY, str(e))
    finally:
        cache[DART_API_KEY] = api_key
        return api_key


@socketio.on(DART_API_KEY)
def api_key_handler(data):
    if isinstance(data, str):
        data = json.loads(data)

    tp = data.get('type', 'GET')
    if not isinstance(tp, str):
        transmit.errors(DART_API_KEY, 'Invalid request type')
        return

    tp = tp.upper()
    api_key = None
    if tp == 'GET':
        config = read_config_file()
        if config:
            api_key = config.get(DART_API_KEY)
    elif tp == 'SET':
        api_key = data.get(DART_API_KEY)
    else:
        transmit.errors(DART_API_KEY, 'Invalid request type')
        return

    api_key = set_api_key(api_key)
    if api_key is not None:
        save_config_file({DART_API_KEY: api_key})

    transmit.data(DART_API_KEY, {DART_API_KEY: api_key})

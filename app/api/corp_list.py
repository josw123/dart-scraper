#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from dart_fss.errors import APIKeyError

from app import socketio
from app.api.api_key import check_authorized
from app.api.globals import transmit, sem, cache, get_dart_fss

# TYPE
CORP_LIST = 'CORP_LIST'


def get_corp_list():
    # Acquire semaphore
    sem.acquire()
    corp_list = []
    dart = get_dart_fss()
    try:
        corp_list = cache.get('corp_list')
        if corp_list is None:
            corp_list = dart.get_corp_list()
            corp_list.load()
        cache['corp_list'] = corp_list
    except APIKeyError as e:
        transmit.errors(CORP_LIST, str(e))
    finally:
        # Release semaphore
        sem.release()
        return corp_list


@socketio.on(CORP_LIST)
def corp_list_handler(data):

    if not check_authorized():
        return

    # Loading Start
    transmit.start(CORP_LIST)
    corp_list = get_corp_list()
    transmit.finish(CORP_LIST)

    if isinstance(data, str):
        data = json.loads(data)

    corp_name = data.get('corp_name')
    exactly = data.get('exactly')

    if corp_name is None:
        transmit.errors(CORP_LIST, 'corp_name is None')
    else:
        corps = corp_list.find_by_corp_name(corp_name=corp_name, exactly=exactly)
        if corps is None:
            corps = []
        transmit.data(CORP_LIST, [x.to_dict() for x in corps])

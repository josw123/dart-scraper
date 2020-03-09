#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import dart_fss as dart

from app import socketio
from app.utils import ThreadSafeDict


class Transmit(object):

    @staticmethod
    def start(tp):
        payload = dict(type='loading', data='start')
        socketio.emit(tp, payload, broadcast=True)

    @staticmethod
    def finish(tp):
        payload = dict(type='loading', data='finish')
        socketio.emit(tp, payload, broadcast=True)

    @staticmethod
    def errors(tp, msg):
        payload = dict(type=tp, data=msg)
        socketio.emit('errors', payload, broadcast=True)

    @staticmethod
    def data(tp, data):
        payload = dict(type='data', data=data)
        socketio.emit(tp, payload, broadcast=True)


transmit = Transmit()
sem = threading.Semaphore()
cache = ThreadSafeDict()
cache['dart'] = dart


def get_dart_fss():
    return cache['dart']




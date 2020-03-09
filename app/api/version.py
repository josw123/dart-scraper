#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import socketio, ver
from app.api.globals import transmit

VERSION = 'VERSION'


@socketio.on(VERSION)
def version_handler():
    transmit.data(VERSION, ver)


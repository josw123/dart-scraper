#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

from flask import Flask
from flask_socketio import SocketIO

# Version
ver = 'v0.4.0'

# Configuration for frozen
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    favicon_folder = template_folder
    js_folder = os.path.join(template_folder, 'js')
    css_folder = os.path.join(template_folder, 'css')
    img_folder = os.path.join(template_folder, 'img')
    app = Flask(__name__, template_folder=template_folder)
else:
    template_folder = os.path.join('..', 'templates')
    favicon_folder = template_folder
    js_folder = os.path.join(template_folder, 'js')
    css_folder = os.path.join(template_folder, 'css')
    img_folder = os.path.join(template_folder, 'img')
    app = Flask(__name__, template_folder=template_folder)

# CORS setting
cors_allowed_origins = '*'

# Generate SocketIo
socketio = SocketIO(app, cors_allowed_origins=cors_allowed_origins)

from app import resource
from app import cors
from app import socketIo
from app import api

__all__ = ['app', 'ver', 'socketio',  'cors_allowed_origins',
           'favicon_folder', 'js_folder', 'css_folder', 'img_folder']

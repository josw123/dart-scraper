#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import app, favicon_folder, js_folder, css_folder, img_folder
from flask import send_from_directory, render_template


@app.route('/favicon.ico')
def favicon():
    """ return favicon """
    return send_from_directory(favicon_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/js/<path:path>')
def send_js(path):
    """ return javascript """
    return send_from_directory(js_folder, path)


@app.route('/css/<path:path>')
def send_css(path):
    """ return css """
    return send_from_directory(css_folder, path)


@app.route('/img/<path:path>')
def send_img(path):
    """ return images """
    return send_from_directory(img_folder, path)


@app.route('/')
def index():
    return render_template('index.html')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
import argparse
import pathlib

import json
import socket
import webbrowser

import version
import dart_fss as dart


from halo import Halo
from flask import Flask, render_template, request, jsonify, make_response, send_from_directory

ver = version.ver

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    favicon_folder = template_folder
    js_folder = os.path.join(template_folder, 'js')
    css_folder = os.path.join(template_folder, 'css')
    img_folder = os.path.join(template_folder, 'img')
    app = Flask(__name__, template_folder=template_folder)
else:
    favicon_folder = 'templates'
    js_folder = 'templates/js'
    css_folder = 'templates/css'
    img_folder = 'templates/img'
    app = Flask(__name__)


def get_config_path():
    if sys.platform == 'darwin':
        app_dir = os.path.join(os.path.expanduser('~/Library/Application Support'), 'dart-scraper')
    elif sys.platform == 'win32':
        app_dir = os.path.join(os.getenv('appdata'), 'dart-scraper')
    else:
        app_dir = os.path.join(os.path.expanduser('~'), '.dart-scraper')
    config_path = os.path.join(app_dir, 'dart-setting.json')
    return app_dir, config_path


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(favicon_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/js/<path:path>')
def send_js(path):
    global js_folder
    return send_from_directory(js_folder, path)


@app.route('/css/<path:path>')
def send_css(path):
    global css_folder
    return send_from_directory(css_folder, path)


@app.route('/img/<path:path>')
def send_img(path):
    global img_folder
    return send_from_directory(img_folder, path)


def save_config_file(api_key):
    app_dir, config_path = get_config_path()
    if not os.path.exists(app_dir):
        app.logger.info("Save folder not found")
        os.makedirs(app_dir)
    
    data = {'API_KEY': api_key}

    with open(config_path, 'w') as config_file:
        json.dump(data, config_file)


def read_config_file():
    app.logger.info('Reading Config file')
    _, config_path = get_config_path()
    if not os.path.exists(config_path):
        app.logger.info('Config file not found')
        return None

    with open(config_path, 'r') as config_file:
        data = json.load(config_file)

    return data['API_KEY']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apikey', methods=['POST', 'GET'])
def key():
    data = {}
    if request.method == 'GET':
        api_key = read_config_file()
        data['api_key'] = api_key

    if request.method == 'POST':
        res_data = request.json
        api_key = res_data.get('api_key')
        if api_key and len(api_key) == 40:
            try:
                dart.dart_set_api_key(api_key)
                save_config_file(api_key)
                data['ret_code'] = 'success'
            except dart.errors.DartAPIError:
                 data['ret_code'] = 'error'
        else:
            data['ret_code'] = 'error'
    return jsonify(data)


@app.route('/version')
def version():
    global ver
    ret_code = {
        'version': ver,
        'ret_code':'success'
    }
    return jsonify(ret_code)


@app.route('/company')
def company():
    data = request.json
    if data is None:
        name = ''
    else:
        name = data.get('name', '')
    crps = crp_list.find_by_name(name)
    
    crps_list = []
    for crp in crps:
        crp_data = {'code': crp.crp_cd, 'name': crp.crp_nm}
        crps_list.append(crp_data)
    
    ret_code = {'ret_code': 'success', 'crp_list': crps_list}
    return jsonify(ret_code)

@app.route('/download' , methods=['POST'])
def download():
    ret_code = {}
    data = request.json
    api_key = data['api_key']
    if api_key is None:
        ret_code['msg'] = 'DART API KEY can not be None or empty'
        ret_code['ret_code'] = 'invalid'
        return  jsonify(ret_code)

    crp_cd = data.get('crp_cd', None)
    if crp_cd is None:
        ret_code['msg'] = 'crp_cd can not be None or empty'
        ret_code['ret_code'] = 'invalid'
        return  jsonify(ret_code)
    
    start_dt = data.get('start_dt', '20120101')
    end_dt = data.get('end_dt', None)
    path = data.get('path', None)
    
    crp = crp_list.find_by_crp_cd(crp_cd)
    if crp is None:
        ret_code['msg'] = 'Invalid crp_cd'
        ret_code['ret_code'] = 'error'
        return  jsonify(ret_code)
    separate = data.get('separate', False)
    report_tp = data.get('report_tp', 'annual')
    report_tp = report_tp.lower()
    
    # Make Folder
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    filename = '{}_{}_{}.xlsx'.format(crp_cd, 'separate' if separate else 'consolidated', report_tp)
    fs = crp.get_financial_statement(start_dt=start_dt, end_dt=end_dt, separate=separate, report_tp=report_tp)
    
    fs.save(path=path,filename=filename)
    ret_code['ret_code'] = 'success'
    ret_code['msg'] = 'Successfully added to download list'
    return jsonify(ret_code)

@app.route('/path', methods=['GET'])
def path():
    ret_code = {}
    ret_code['path'] = os.path.join(os.getcwd(),'fsdata')
    ret_code['ret_code'] = 'success'
    return jsonify(ret_code)

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response


parser = argparse.ArgumentParser(description=' Dart-Scraper')
parser.add_argument('-p', '--port', type=int, help="Dart-Scraper port")
args = vars(parser.parse_args())
port = args.get('port')
if port is None:
    port = 5000
    
spinner = Halo(text='Downloading list of companies', spinner='dots')
spinner.start()
crp_list = dart.get_crp_list()
spinner.stop()

url = "http://127.0.0.1:{}".format(port)
webbrowser.open_new(url)
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
app.config['JSON_AS_ASCII'] = False
app.run(host='127.0.0.1', port=port)


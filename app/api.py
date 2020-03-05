#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import dart_fss as dart

from app import app, ver
from flask import request, jsonify
from app.utils import read_config_file, save_config_file
from app.socketIo import corp_list_loading

@app.route('/key', methods=['POST', 'GET'])
def dart_api_key():
    """ Read or Save DART API KEY"""
    data = {}
    if request.method == 'GET':
        configuration = read_config_file()
        if configuration:
            data['api_key'] = configuration.get('DART_API_KEY')
        else:
            data['api_key'] = None

    if request.method == 'POST':
        res_data = request.json
        api_key = res_data.get('api_key')
        if api_key:
            try:
                dart.set_api_key(api_key)
                save_config_file({'DART_API_KEY': api_key})
                data['ret_code'] = 'success'
            except dart.errors.APIKeyError:
                data['ret_code'] = 'error'
                data['msg'] = 'Invalid API Key'
        else:
            data['ret_code'] = 'error'
            data['msg'] = 'API key is empty'
    return jsonify(data)


@app.route('/version')
def version():
    """ Get Current Version """
    ret_code = {
        'version': ver,
        'ret_code': 'success'
    }
    return jsonify(ret_code)


@app.route('/dir', methods=['POST'])
def directory():
    res_data = request.get_json()
    if res_data is not None:
        base_path = res_data.get('base_path', os.getcwd())
        new_path = res_data.get('new_path')
        if new_path is not None:
            base_path = os.path.abspath(os.path.join(base_path, new_path))
    else:
        base_path = os.getcwd()

    if not os.path.isdir(base_path):
        ret_code = {
            'ret_code': 'error',
            'msg': 'invalid path',
        }
        return jsonify(ret_code)

    path = os.path.join(base_path, '*\\')
    subdir = []
    for d in glob.glob(path):
        subdir.append(d)
    ret_code = {
        'ret_code': 'success',
        'base_path': base_path,
        'subdir': subdir,
    }
    return jsonify(ret_code)

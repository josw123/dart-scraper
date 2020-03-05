#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import threading


def get_config_path():
    """ Get Configuration Path

    Returns
    -------
    tuple of str
        app directory, configuration path
    """
    if sys.platform == 'darwin':
        app_dir = os.path.join(os.path.expanduser('~/Library/Application Support'), 'dart-scraper')
    elif sys.platform == 'win32':
        app_dir = os.path.join(os.getenv('appdata'), 'dart-scraper')
    else:
        app_dir = os.path.join(os.path.expanduser('~'), '.dart-scraper')
    config_path = os.path.join(app_dir, 'dart-setting.json')
    return app_dir, config_path


def save_config_file(data):
    """ Save configuration file

    Parameters
    ----------
    data: dict
        data to save
    """
    app_dir, config_path = get_config_path()
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)

    with open(config_path, 'w') as config_file:
        json.dump(data, config_file)


def read_config_file():
    """ Read configuration file

    Returns
    -------
    dict
        configuration data
    """
    _, config_path = get_config_path()
    if not os.path.exists(config_path):
        return None

    with open(config_path, 'r') as config_file:
        data = json.load(config_file)

    return data


class ThreadSafeDict(dict):
    def __init__(self, * p_arg, ** n_arg):
        dict.__init__(self, * p_arg, ** n_arg)
        self._lock = threading.Lock()

    def __enter__(self) :
        self._lock.acquire()
        return self

    def __exit__(self, type, value, traceback):
        self._lock.release()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import webbrowser


from app import socketio, app, set_cors
from app.utils import read_config_file

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=' Dart-Scraper')
    parser.add_argument('-p', '--port', type=int, help="Dart-Scraper port")
    args = vars(parser.parse_args())
    port = args.get('port')
    if port is None:
        config = read_config_file()
        if config is not None:
            port = int(config.get('port', 5000))
        else:
            port = 5000

    url = "http://127.0.0.1:{}".format(port)
    set_cors(url)
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = 'secret_key'

    # Open Web Browser
    webbrowser.open_new(url)
    socketio.run(app, host='127.0.0.1', port=port, debug=False)

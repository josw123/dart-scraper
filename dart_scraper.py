#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import webbrowser

from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon, QFont

from app import socketio, app, set_cors


class MainWidget(QWidget):

    def __init__(self, width=200, height=50):
        super().__init__()
        if getattr(sys, 'frozen', False):
            favicon = os.path.join(sys._MEIPASS, 'templates', 'favicon.ico')
        else:
            favicon = os.path.join('.', 'templates', 'favicon.ico')
        self.favicon = favicon
        self.initUI(width, height)

    def initUI(self, width, height):
        # Set Window
        self.setFixedSize(200, 50)
        self.setWindowTitle('Dart-Scraper')
        self.setWindowIcon(QIcon(self.favicon))
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # Set Button
        btn = QPushButton('Quit', self)
        btn.setFixedSize(width, height)

        # Set Button Font
        font = QFont('Roboto')
        font.setPointSize(14)
        font.setBold(True)
        btn.setFont(font)

        # Set Button Click
        btn.clicked.connect(self.close)
        self.show()


class FlaskThread(QThread):
    def __init__(self, socketio, app, host, port):
        super().__init__()
        self.socketio = socketio
        self.app = app
        self.host = host
        self.port = port

    def __del__(self):
        self.wait()

    def run(self):
        self.socketio.run(self.app, host=self.host, port=self.port)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=' Dart-Scraper')
    parser.add_argument('-p', '--port', type=int, help="Dart-Scraper port")
    args = vars(parser.parse_args())
    port = args.get('port')
    if port is None:
        port = 5000

    url = "http://127.0.0.1:{}".format(port)
    set_cors(url)
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = 'secret_key'

    # socketio.run(app, host='127.0.0.1', port=port, debug=False)
    qApplication = QApplication(sys.argv)

    # Start Flask
    webapp = FlaskThread(socketio, app, '127.0.0.1', port)
    webapp.start()
    qApplication.aboutToQuit.connect(webapp.terminate)

    # Open Web Browser
    webbrowser.open_new(url)

    # PyQt Widget
    w = MainWidget()
    sys.exit(qApplication.exec_())

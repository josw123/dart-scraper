#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import app, cors_allowed_origins


@app.after_request
def after_request(response):
    """ Disable CORS """
    response.headers.add('Access-Control-Allow-Origin', cors_allowed_origins)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

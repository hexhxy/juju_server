##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import logging
import subprocess

import re
from flask import jsonify
from flask import make_response

from app import app

logger = logging.getLogger('juju')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

hdlr = logging.FileHandler('juju_app.log')
hdlr.setFormatter(formatter)
hdlr.setLevel(logging.DEBUG)
logger.addHandler(hdlr)


@app.route('/')
def index():
    return "Hello, Juju Client VM!"


@app.route('/api/v1/model/status')
def model_status():
    cmd = 'juju status'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)
    clearwater_started = False
    while p.poll() is None:
        line = p.stdout.readline().rstrip()
        logger.debug(line)
        if re.search('clearwater', line):
            clearwater_started = True
            break
    if not clearwater_started:
        response = {'msg': ('Clearwater is not found, '
                            'it maybe not started or there is some error.')}
    else:
        cmd = 'juju status | grep idle | wc -l'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        while p.poll() is None:
            line = p.stdout.readline().rstrip()
            if str(line) == '7':
                response = {'msg': 'Clearwater has fully started'}
            else:
                response = {'msg': '%s out of 7 nodes have started' %
                            str(line)}

    resp = make_response(jsonify(response))
    return resp


@app.route('/api/v1/model/output')
def model_output():
    return 'hi output'

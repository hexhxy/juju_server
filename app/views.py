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
        print(line)
        if re.search('clearwater', line):
            clearwater_started = True
            break
    if not clearwater_started:
        response = {'msg': ('Clearwater is not found, '
                            'it maybe not started or there is some error.')}
        response['vnf_alive'] = False
    else:
        cmd = 'juju status | grep idle | wc -l'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        while p.poll() is None:
            line = p.stdout.readline().rstrip()
            if str(line) == '7':
                response = {
                                'msg': 'Clearwater has fully started',
                                'vnf_alive': True
                            }
            elif line:
                response = {'msg': '%s out of 7 nodes have started' %
                            str(line)}
                response['vnf_alive'] = False

    resp = make_response(jsonify(response))
    return resp


@app.route('/api/v1/model/output')
def model_output():
    data = {}
    response = {}
    cmd = 'juju status | grep clearwater-ellis | grep tcp | awk "{print \$5}"'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)
    ellis_ip_found = False
    while p.poll() is None:
        line = p.stdout.readline().rstrip()
        print(line)
        if line:
            print('Ellis internal IP: %s' % line)
            cmd = ('. /home/ubuntu/admin-openrc.sh;'
                   'openstack server list | grep {0}').format(line)

            cmd += '| awk "{print \$9}"'
            print(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, shell=True)
            while p.poll() is None:
                line = p.stdout.readline().rstrip()
                if line:
                    print('Ellis external IP: %s' % line)
                    data['ellis_ip'] = line
                    ellis_ip_found = True
        else:
            response = {'msg': 'Clearwater is not started or there is some errror.'}

    if not ellis_ip_found:
        response = {'msg': 'Error with getting Ellis IP'}

    cmd = 'juju status | grep clearwater-bono | grep tcp | awk "{print \$5}"'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)
    bono_ip_found = False
    while p.poll() is None:
        line = p.stdout.readline().rstrip()
        print(line)
        if line:
            print('Bono internal IP: %s' % line)
            cmd = ('. /home/ubuntu/admin-openrc.sh;'
                   'openstack server list | grep {0}').format(line)

            cmd += '| awk "{print \$9}"'
            print(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, shell=True)
            while p.poll() is None:
                line = p.stdout.readline().rstrip()
                if line:
                    print('Bono external IP: %s' % line)
                    data['bono_ip'] = line
                    bono_ip_found = True
        else:
            response = {'msg': 'Clearwater is not started or there is some errror.'}

    if not bono_ip_found:
        response = {'msg': 'Error with getting Bono IP'}

    cmd = 'juju status | grep dns | grep tcp | awk "{print \$5}"'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)
    dns_ip_found = False
    while p.poll() is None:
        line = p.stdout.readline().rstrip()
        print(line)
        if line:
            print('DNS internal IP: %s' % line)
            cmd = ('. /home/ubuntu/admin-openrc.sh;'
                   'openstack server list | grep {0}').format(line)

            cmd += '| awk "{print \$9}"'
            print(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, shell=True)
            while p.poll() is None:
                line = p.stdout.readline().rstrip()
                if line:
                    print('DNS external IP: %s' % line)
                    data['dns_ip'] = line
                    dns_ip_found = True
        else:
            response = {'msg': 'Clearwater is not started or there is some errror.'}

    if not dns_ip_found:
        response = {'msg': 'Error with getting DNS IP'}

    response['data'] = data
    resp = make_response(jsonify(response))
    return resp

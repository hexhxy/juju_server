#!/bin/bash
##############################################################################
# Copyright (c) 2016-2017 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
sudo apt-get install python-virtualenv
pip install virtualenv
virtualenv flask
source flask/bin/activate
pip install flask==0.11.1
pip install flask-restful==0.3.5

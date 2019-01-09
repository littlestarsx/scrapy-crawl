#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
import os

def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/db_config.py'
    config.read(path)
    return config.get(section, key)

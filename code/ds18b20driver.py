#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def find_sensors(basedir):
    return [x for x in os.listdir(basedir) if x.startswith('28')]


def read_temp(sensor):
    with open(sensor + '/w1_slave', "r") as f:
        data = f.readlines()

    if data[0].strip()[-3:] == "YES":
        return [True, float(data[1].split("=")[1])]
    else:
        return [False, 0.0]  

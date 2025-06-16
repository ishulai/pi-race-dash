#!/bin/bash
cd /home/pi/pi-race-dash
PYTHONPATH=. /usr/bin/python3 dash.py >> /home/pi/app.log 2>&1
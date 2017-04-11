#!/bin/bash
screen -S "mal9000" -d -m
screen -r "mal9000" -X stuff $'python jasper/jasper.py\n'

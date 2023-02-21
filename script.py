#!/usr/bin/python3
import os
import webbrowser
command = 'python3 manage.py runserver 127.0.0.1:8000'
hostport = '127.0.0.1:8000/'
path = "./GeoServerDjango/"

os.chdir(path)
os.system(command)

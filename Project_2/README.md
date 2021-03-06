Author:Sharanjeet Singh Mago & Yasir Aslam Shah


Embedded Interface Design - Fall 2018
Project 2


This project is written in Python 3 for interfacing Humidity and Temperature sensor DHT22 with a graphical User Interface that displays data on the GUI.The project is mainly designed into a Python/QT based module that displays data for minimum , maximum , average and current temperature as well as humidity values on a GUI interface.This project exploits SQL in this module to store the humidity and temperature values in two different tables.The GUI is constructed using PyQt5 and is designed using QT designer.The GUI contains various push buttons and to refresh the system and display current temperature and humidity.The average temperature and humidity is also displayed in the GUI that refreshed automatically after every 5 seconds, calculating the overall minimum and maximum values.The tables are sent to a web client using web sockets.The tables are fetched at client side and are displayed on a webpage.

Basic Requirements:

1.Current,Average, Minimum and Maximum Temperature/Humidity on every time interval of 5 seconds

2.The error message 'NOT CONNECTED' displayed when the sensor is not connected

3.Table creation using SQL

4.Table sharing with web server

5.Web page implementation, displaying data parameters upon request

Extra Credits:

1.Secure webpage login

2.Improved UI using CSS elements

3.Temperature data available in F and K scales

Build Steps:
The GUI file (project1.ui) and the python code (pro.py) is saved in the same file and can be run using command line as :sudo Python3 pro.py
The GUI can be closed and exited using close button at the top right of top bar
The web server is run as sudo python3 server.py
The webpage is initialised by opening project2.html

Refrence links:

1.https://www.geeksforgeeks.org/sql-using-python/

2.https://www.python-course.eu/sql_python.php

3.https://circuitpython.readthedocs.io/projects/dht/en/latest/

4.https://github.com/adafruit/circuitpython

5.https://www.w3school.com

"""
@Author Sharanjeet Singh mango
@Brief This python project creates a GUI to show current and
        humidity from a sensor interfaced with Raspberry Pi.
"""

# Importing Libraries
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QTimer
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi
import Adafruit_DHT
from time import strftime

# Class for login functionality
class login(QDialog):
    def __init__(self):
        super(login,self).__init__()
        loadUi('login.ui',self)
        self.setWindowTitle('Login')
        self.pushButton_login.clicked.connect(self.login_check)

#login check
    def login_check(self):
        caca = self.lineEdit_username.text()
        if self.lineEdit_username.text() == "mango" and self.lineEdit_password.text() == "mango":
            self.accept()
            self.label_login.setText("Login Successful")
        else:
            self.label_login.setText("Incorrect Details")

# Class for normal software
class pika_class(QDialog):
    def __init__(self):
        super(pika_class,self).__init__()
        loadUi('pika.ui',self)
        self.setWindowTitle('Pika PyQt5 GUI')
        #self.pushButton.clicked.connect(self.on_pushButton_clicked)

#setting up the timer for autorefresh functionality
        self._status_update_timer = QTimer(self)
        self._status_update_timer.setSingleShot(False)
        self._status_update_timer.timeout.connect(self.on_pushButton_clicked)
        self._status_update_timer.start(5000)

    @pyqtSlot()
    def on_pushButton_clicked(self):
#reading the data from the Sensor
        humidity, temperature = Adafruit_DHT.read(22, 4)
#Displaying the time stamp
        t=strftime("%H"+":"+"%M"+":"+"%S")
        self.label_time_value.setText(t)
#Handling disconnection of the sensor
        if temperature is not None and humidity is not None:
#Setting alarm values
            temp_alarm = self.spinBox_temp.value()
            humidity_alarm = self.spinBox_humidity.value()

            if temperature > temp_alarm and humidity < humidity_alarm:
                self.label_status_value.setText("Warning!! High Temp and Low Humidity")
            elif temperature > temp_alarm:
                self.label_status_value.setText("Warning!! High Temp")
            elif humidity < humidity_alarm:
                self.label_status_value.setText("Warning!! Low Humidity")
            else:
                self.label_status_value.setText("Sensor Connected")

            unit = self.comboBox_temp_unit.currentText()
#Checking for units to display
            if unit=="Celsius":
                self.label_temp_value.setText('{0:0.1f}'.format(temperature))
            elif unit=="Fahrenheit":
                temp_f = (temperature*1.8)+ 32
                self.label_temp_value.setText('{0:0.1f}'.format(temp_f))
            elif unit=="Kelvin":
                temp_k = temperature + 273.15
                self.label_temp_value.setText('{0:0.1f}'.format(temp_k))
            else:
                self.label_temp_value.setText("Unit not rec")

            self.progressBar_temp.setValue(temperature)

            self.label_humidity_value.setText('{0:0.1f}'.format(humidity))

            self.progressBar_humidity.setValue(humidity)

        else:
            humidity = 0
            temperature = 0
            self.label_temp_value.setText('{0:0.1f}'.format(temperature))
            self.label_humidity_value.setText('{0:0.1f}'.format(humidity))
            self.label_status_value.setText("Sensor Disconnected")

app=QApplication(sys.argv)
login_widget=login()
login_widget.show()

if login_widget.exec_() == QtWidgets.QDialog.Accepted:
    widget=pika_class()
    widget.show()
    sys.exit(app.exec_())

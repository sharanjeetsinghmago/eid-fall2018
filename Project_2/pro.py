#Author: Yasir Aslam Shah
#Project 1
#EID Ecen 5013
#Fall 2018

import sys
import Adafruit_DHT
import datetime
import calendar
#import matplotlib
import MySQLdb
#matplotlib.use("Qt5Agg")
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.uic import loadUi
from PySide.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
a=5
u=str(a)
db=MySQLdb.connect(host="localhost",user="root",passwd="root",db="pythonspot")
cur=db.cursor()
#cur.execute("SELECT *FROM temp1")
#for row in cur.fetchall():
#    print(row[0],"",row[1],"",row[2],"",row[3],"",row[4],"",row[5])
#print("____________________________________________________________")
#cur.execute("SELECT *FROM hum1")
#for row in cur.fetchall():
#    print(row[0],"",row[1],"",row[2],"",row[3],"",row[4],"",row[5])
    
flag=[]
listA=[]
listB=[]
count1=[]
count2=[]
array_average1=[0,0,0,0]
array_average2=[0,0,0,0]
average1=0
average2=0
timer_temp1='0'
timer_temp2='0'
mintemp=100
maxtemp=0
minhum=100
maxhum=0
str_average1=0.0
str_average2=0.0
min
#function to call calender  
cal1=calendar.month(2018,10)
today=datetime.date.today()
date=format(today)
#connection.close()
#to initailise graph2 to display the average of humidity values                
class project(QDialog):
    def __init__(self):
        super(project,self).__init__()
        loadUi ('projectl.ui',self)
        self.setWindowTitle('ProjectOne')
        self.pushButton1.clicked.connect(self.on_pushButton1_clicked)
        self.pushButton2.clicked.connect(self.on_pushButton2_clicked)
        self.pushButton3.clicked.connect(self.on_pushButton3_clicked)
        humidity,temperature = Adafruit_DHT.read(22,4)
        if humidity == None:#if the sensor is not connected the console prints an error message
            self.label_Hum1.setText("Not Connected")
            self.label_Temp1.setText("Not Connected") 
        self.average_hum()
        self.average_temp()
        #self.main_widget = QWidget(self)
        #self.main_widget1 = QWidget(self)
        #l = QVBoxLayout(self.main_widget)
        #self.main_widget.setGeometry(QtCore.QRect(50,450,200,150))
        #dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        #l.addWidget(dc)
        #t = QVBoxLayout(self.main_widget1)
        #self.main_widget1.setGeometry(QtCore.QRect(250,450,200,150))
        #sc = MyDynamicMplCanvas1(self.main_widget1, width=5, height=4, dpi=100)
        #t.addWidget(sc)
        self.lineEdit.setText("0")
        self.lineEdit1.setText("0")
    @pyqtSlot()
    #date1=format(today)
    #self.label_Time.setText(str(date))
    #function to derive the average of humidity and display the average after every two seconds.
    #the values are automatically displayed on the graphic userinterface
    #the average values is stored in a global varaible and is also dislayed on graph
    def average_hum(self):   
        try:
            self.label_Time.setText(str(date))
            self.label_2.setText(cal1)
            #print(cal1)
            global average1
            global timer_temp2
            global minhum
            global maxhum
            global str_average1
            #global array_average1[]
            humidity,temperature = Adafruit_DHT.read(22,4)
            if humidity == None:#if the sensor is not connected the console prints an error message
                self.label_Hum1.setText("Not Connected")
                cur_hum="NC"
                #hum=0
                cur.execute("SELECT * FROM hum2 ORDER by id DESC LIMIT 1")
                for row in cur.fetchall():
                    minhum=float(row[4])
                    maxhum=float(row[5])
                    str_average1=float(row[2])
            
                #hum=round(humidity,3)
            else:    
                #print('Humidity ={0:0.1f}%'.format(humidity))
                hum=round(humidity,3)
                cur_hum=str(hum)
                listA.append(hum)                
                sum1=sum(listA)
                #print(sum1)
                #print('Timestamp : {:%H:%M:%S}'.format(datetime.datetime.now()))
                #print('Date :{:%Y-%m-%d}'.format(datetime.datetime.now()))
                length1=len(listA)
                average1=sum1/length1
                aver=round(average1,3)
                str_average1=str(aver)
                array_average1.append(average1)
                #print('Hum_average is')
                #print(array_average1)
                self.label_AveA1.setText(str(average1))
                a=1
                count1.append(a)
                counter1=sum(count1)
                if counter1 == 10:
                    listA.clear()
                    #print('yaha')
                    count1.clear()
                if minhum > hum:
                    minhum=hum
                if maxhum < hum:
                    maxhum=hum
            timer_hum =(datetime.datetime.now().strftime('%H:%M:%S'))
            self.label_Time1.setText(str(timer_hum))
            timer_temp2=str(timer_hum)
            
            cur.execute("""INSERT INTO hum2 (col1,col2,col3,col4,col5) VALUES (%s,%s,%s,%s,%s)""",(cur_hum,str_average1,timer_temp2,minhum,maxhum,))
            db.commit();
            cur.execute("SELECT *FROM hum2")
            for row in cur.fetchall():
                print(row[0  ],"",row[1  ]," ",row[2  ]," ",row[3  ]," ",row[4  ]," ",row[5  ])
 
        finally:
            QtCore.QTimer.singleShot(5000,self.average_hum)#the average function for humidity is called after every 2 sec 
    #function to calculate the average temperture values automatically after every 2.5 seconds
    #the avergae function is used also to feed the graph to display the values every 10 seconds
    def average_temp(self):
        try:
            global average2
            global timer_temp1
            global mintemp
            global maxtemp
            global str_average2
            humidity,temperature = Adafruit_DHT.read(22,4)
            #print('yasir')
            if temperature == None:#if the sensor is not connected, an error message is displayed on UI
                self.label_Temp1.setText("Not Connected")
                cur_temp="NC"
                #temp=0
                far_temp=0
                kel_temp=0
                cur.execute("SELECT * FROM temp2 ORDER by id DESC LIMIT 1")
                for row in cur.fetchall():
                    mintemp=float(row[4])
                    maxtemp=float(row[5])
                    str_average2=float(row[2])
            else:
                #print('Temperature ={0:0.f}*'.format(temperature))
                temp=round(temperature,3)
                cur_temp =str(temp)
                #cur.execute("""INSERT INTO temperature1 (col1) VALUES (%s)""",(cur_temp,))                
                #db.commit();
                listB.append(temp)
                sum2=sum(listB)
                #print(sum2)
                length2=len(listB)
                average2=(sum2/length2)
                averB=round(average2,3)
                str_average2=str(averB)
                if mintemp > temp:
                    mintemp=temp
                if maxtemp < temp:
                    maxtemp=temp
                far_temp=((((temp)*9)/5)+32)
                kel_temp=(273.0+(temp))
           
            timer_temp=(datetime.datetime.now().strftime('%H:%M:%S'))
            self.label_Time2.setText(str(timer_temp))
            timer_temp1=str(timer_temp)
            cur.execute("""INSERT INTO temp2 (col1,col2,col3,col4,col5,col6,col7) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(cur_temp,str_average2,timer_temp1,mintemp,maxtemp,far_temp,kel_temp,))
            db.commit();
                #for row in cur.fetchall():
                    #print(row[0],"",row[1],"",row[2],"",row[3],"",row[4],"",row[5])
            cur.execute("SELECT *FROM temp2")
            for row in cur.fetchall():
                print( row[   0] ,"   ",row[   1] ,"   ",row[   2 ],"   ",row[   3] ,"   ",row[   4],"   ",row[   5],"   ",row[6],"   ",row[7])
            #print("_________________________________________________________________________")
            array_average2.append(average2)
            #print('Temp_average')
            #print(average2)
            self.label_AveB1.setText(str(average2))
            b=1
            count2.append(b)
            counter2=sum(count2)
            #print(counter2)
            #after ten entries the array is cleared
            if counter2 == 10:
                listB.clear()
                #print('waha')
                count2.clear()
        finally:
            #this function is called to display average temperature every 2.5 seconds
            QtCore.QTimer.singleShot(5000,self.average_temp)
    #function defined at clicking pushbutton1(Refresh) to display current temperature
    #in celsuis, farenheut and kelvin.The curent temp is displayed with a timestamp
    def on_pushButton1_clicked(self):
        timer_temp=(datetime.datetime.now().strftime('%H:%M:%S'))
        self.label_Time2.setText(str(timer_temp))
        #cur.execute("""INSERT INTO temperature1 (col5) VALUES (%s)""",(timer_temp,))
        #db.commit();
        humidity,temperature = Adafruit_DHT.read(22,4)
        #farenhiet=((temperature *9)/5 + 32) #for temperature conversion to farenhiet
        if temperature == None:#if sensor is not connected, an error message is displayed
            self.label_Temp1.setText("Not Connected")
        else:
            #print('Temp ={0:0.1f}*'.format(temperature))
            self.label_Temp1.setText(str(temperature))
            comp2=self.lineEdit1.text()
            if comp2 == None:
                self.label_AlertA.setText('Set Threshold')
            else:   
                compare2=int(comp2)
                if compare2 > temperature:
                    self.label_AlertB.setText('Less Alert!')

                else:
                    self.label_AlertB.setText('More Alert!')
            #cur.execute("SELECT *FROM temp1")
            #for row in cur.fetchall():
                #print(row[0],"",row[1],"",row[2],"",row[3],"",row[4],"",row[5])

            temp=temperature
            listB.append(temp)
    #function defined at pushbutton clicked(Refresh) to display the current humidity.The humidity 
    #is displayed with current timestamp
    def on_pushButton2_clicked(self):
        #displaying time stamp
        timer_hum =(datetime.datetime.now().strftime('%H:%M:%S'))
        self.label_Time1.setText(str(timer_hum))
        humidity,temperature = Adafruit_DHT.read(22,4)
        if humidity == None:
            #if the humidty sensor is not connected an error is displayed as not connected
            self.label_Hum1.setText("Not Connected")
        else:    
            self.label_Hum1.setText(str(humidity))
            #print('Humidity ={0:0.1f}%'.format(humidity))
            hum=humidity
            listA.append(hum)
            comp1=self.lineEdit.text()
            #print(comp1)
            #compare1 = int(comp1)
            if comp1 == None:
                self.label_AlertA.setText('Set Threshold')
            else:
                compare1=int(comp1)
                if compare1 > humidity:
                    self.label_AlertA.setText('Less Alert!')
                else:
                    self.label_AlertA.setText('More Alert!')
            #cur.execute("SELECT *FROM hum1")
            #for row in cur.fetchall():
                #print(row[0],"",row[1],"",row[2],"",row[3],"",row[4],"",row[5])
       
    #pushbutton 3 is used to display the current temperature in farenheit        
    def on_pushButton3_clicked(self):
        humidity,temperature = Adafruit_DHT.read(22,4)
        if temperature == None:
            self.label_Temp1.setText("Not Connected")
        else:
            farenhiet=((temperature*9)/5 + 32)
            self.label_Temp1.setText(str(farenhiet))
    #pushbutton 4 is used to display the current temperature in kelvin     
    def on_pushButton4_clicked(self):
        humidity,temperature = Adafruit_DHT.read(22,4)
        if temperature == None:
            self.label_Temp1.setText("Not Connected")
        else:
            kelvin=temperature+273 
            self.label_Temp1.setText(str(kelvin))
    #pushbutton 5 is clicked to display temperature in celsius     
    def on_pushButton5_clicked(self):
        humidity,temperature = Adafruit_DHT.read(22,4)
        if temperature == None:
            self.label_Temp1.setText("Not Connected")
        else:
            self.label_Temp1.setText(str(temperature)) 


app=QApplication(sys.argv)
widget=project()
widget.show()
sys.exit(app.exec_())




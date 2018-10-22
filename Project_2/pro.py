#Author: Sharanjeet Singh Mago & Yasir Aslam Shah
#Project 2
#EID Ecen 5013
#Fall 2018
#
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
#connecting to pythonspot
db=MySQLdb.connect(host="localhost",user="root",passwd="root",db="pythonspot")
cur=db.cursor()
#global variables    
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
kel=0
far=0
cel=1

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
            self.labelHUM.setText("Not Connected")
            self.labelTEMP.setText("Not Connected") 
            d=99
        self.average_hum()
        self.average_temp()
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
            global kel
            global far
            global cel

            #global array_average1[]
            humidity,temperature = Adafruit_DHT.read(22,4)
            if humidity == None:#if the sensor is not connected the console prints an error message
                #self.label_Hum1.setText("
                cur_hum="NC"                
                self.labelHUM.setText("Not Connected") 
                cur.execute("SELECT * FROM hum2 ORDER by id DESC LIMIT 1")
                for row in cur.fetchall():
                    minhum=float(row[4])
                    maxhum=float(row[5])
                    str_average1=float(row[2])
                    
                #hum=round(humidity,3)
            else:    
                self.labelHUM.setText("Connected") 
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
                self.label_AveA1.setText(str(str_average1))
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
            self.label_curr_hum.setText(str(cur_hum))
            self.label_min_hum.setText(str(minhum))
            self.label_max_hum.setText(str(maxhum))
            timer_temp=(datetime.datetime.now().strftime('%H:%M:%S'))
            self.label_Time2.setText(str(timer_temp))
            #inserting into table HUM@
            cur.execute("""INSERT INTO hum2 (col1,col2,col3,col4,col5) VALUES (%s,%s,%s,%s,%s)""",(cur_hum,str_average1,timer_temp2,minhum,maxhum,))
            db.commit();
            #printing values off table HUM2
            #cur.execute("SELECT *FROM hum2")
            cur.execute("SELECT * FROM hum2 ORDER by id DESC LIMIT 1")
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
            global kel
            global far
            global cel
            humidity,temperature = Adafruit_DHT.read(22,4)
            #print('yasir')
            if temperature == None:#if the sensor is not connected, an error message is displayed on UI
                #self.label_Temp1.setText("Not Connected")
                cur_temp="NC"
                #temp=0
                far_temp=0
                self.labelTEMP.setText("Not Connected")    
                self.label_curr_temp.setText(str(cur_temp))

                kel_temp=0
                cur.execute("SELECT * FROM temp2 ORDER by id DESC LIMIT 1")
                for row in cur.fetchall():
                    mintemp=float(row[4])
                    maxtemp=float(row[5])
                    str_average2=float(row[2])
            else:
                #print('Temperature ={0:0.f}*'.format(temperature))
                self.labelTEMP.setText("Connected")
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
                #print(kel)
                #print(far)
                #print(cel)

                array_average2.append(average2)            
                if ((kel==1)&(far==0)&(cel==0)):
                    #print("k mai gusa")
                    mintempK=(float(mintemp)+273.0)
                    maxtempK=(float(maxtemp)+273.0)
                    str_average2K=(float(str_average2)+273.0)
                    cur_tempK=(float(cur_temp)+273.0)
                    average2K=(float(average2)+273.0)
                    self.label_curr_temp.setText(str(cur_tempK))
                    self.label_min_temp.setText(str(mintempK))
                    self.label_max_temp.setText(str(maxtempK))
                    self.label_AveB1.setText(str(average2K))

                if ((kel==0)&(far==1)&(cel==0)):
                    #print("f mai gusa")
                    mintempF=((float(mintemp)/9)*5 + 32)
                    maxtempF=((float(maxtemp)/9)*5 + 32)
                    str_average2F=((float(str_average2)/9)*5 + 32)
                    cur_tempF=((float(cur_temp)/9)*5 + 32)
                    average2F=((float(average2)/9)*5 + 32)
                    self.label_curr_temp.setText(str(cur_tempF))
                    self.label_min_temp.setText(str(mintempF))
                    self.label_max_temp.setText(str(maxtempF))
                    self.label_AveB1.setText(str(average2F))


                if ((kel==0)&(far==0)&(cel==1)):
                    self.labelscale.setText("Celsius")
                    #print("c mai gusa")
                    self.label_curr_temp.setText(str(cur_temp))
                    self.label_min_temp.setText(str(mintemp))
                    self.label_max_temp.setText(str(maxtemp))
                    self.label_AveB1.setText(str(average2))


            timer_temp=(datetime.datetime.now().strftime('%H:%M:%S'))
            timer_temp1=str(timer_temp)
            self.label_Time2.setText(str(timer_temp1))
            cur.execute("""INSERT INTO temp2 (col1,col2,col3,col4,col5,col6,col7) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(cur_temp,str_average2,timer_temp1,mintemp,maxtemp,far_temp,kel_temp,))
            db.commit();
                #for row in cur.fetchall():
                    #print(row[0],"",row[1],"",row[2],"",row[3],"",row[4],"",row[5])
            cur.execute("SELECT * FROM temp2 ORDER by id DESC LIMIT 1")
            #cur.execute("SELECT *FROM temp2")
            for row in cur.fetchall():
                print( row[   0] ,"   ",row[   1] ,"   ",row[   2 ],"   ",row[   3] ,"   ",row[   4],"   ",row[   5],"   ",row[6],"   ",row[7])
            #print('Temp_average')
            #print(average2)
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
        #timer_temp=(datetime.datetime.now().strftime('%H:%M:%S'))
        #self.label_Time2.setText(str(timer_temp))
        #cur.execute("""INSERT INTO temperature1 (col5) VALUES (%s)""",(timer_temp,))
        #db.commit();
        humidity,temperature = Adafruit_DHT.read(22,4)
        #farenhiet=((temperature *9)/5 + 32) #for temperature conversion to farenhiet
        if temperature == None:#if sensor is not connected, an error message is displayed
            #self.label_Temp1.setText("Not Connected")
            self.labelTEMP.setText("Not Connected")    
            self.label_curr_temp.setText("NC")

        else:
            self.labelTEMP.setText("Connected")    
            #self.label_curr_temp.setText(str(cur_temp))

            #print('Temp ={0:0.1f}*'.format(temperature))
            #self.label_Temp1.setText(str(temperature))
            comp2=self.lineEdit1.text()
            if comp2 == None:
                self.label_AlertA.setText('Set Threshold')
            else:   
                compare2=int(comp2)
                if compare2 > temperature:
                    self.label_AlertB.setText('Cold!')

                else:
                    self.label_AlertB.setText('Hot!')
            #cur.execute("SELECT *FROM temp1")
            #for row in cur.fetchall():
                #print(row[0],"",row[1],"",row[2],"",row[3],"",row[4],"",row[5])

            temp=temperature
            listB.append(temp)
    #function defined at pushbutton clicked(Refresh) to display the current humidity.The humidity 
    #is displayed with current timestamp
    def on_pushButton2_clicked(self):
        #displaying time stamp
        #timer_hum =(datetime.datetime.now().strftime('%H:%M:%S'))
        #self.label_Time1.setText(str(timer_hum))
        humidity,temperature = Adafruit_DHT.read(22,4)
        if humidity == None:
            #if the humidty sensor is not connected an error is displayed as not connected
            #self.label_Hum1.setText("Not Connected")
            d=8
        else:    
            #self.label_Hum1.setText(str(humidity))
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
                    self.label_AlertA.setText('Dry!')
                else:
                    self.label_AlertA.setText('Humid!')
            #cur.execute("SELECT *FROM hum1")
            #for row in cur.fetchall():
                #print(row[0],"",row[1],"",row[2],"",row[3],"",row[4],"",row[5])
       
    #pushbutton 3 is used to display the current temperature in farenheit        
    def on_pushButton3_clicked(self):#kelvin selection
        global kel
        global far
        global cel
        humidity,temperature = Adafruit_DHT.read(22,4)
        #print("Klevin selected\n")
        self.labelscale.setText("Kelvin")
        if temperature == None:
            #self.label_Temp1.setText("Not Connected")
            kel=1
            far=0
            cel=0
        else:
            kel=1
            far=0
            cel=0
        # print(kel)
        #print(far)
        #print(cel)
    
    #pushbutton 4 is used to display the current temperature in kelvin     
    def on_pushButton4_clicked(self):#farenheit is selcted
        global kel
        global far
        global cel
        humidity,temperature = Adafruit_DHT.read(22,4)
        self.labelscale.setText("Farenheit")
        print("farenheight\n")
        if temperature == None:
            #self.label_Temp1.setText("Not Connected")
            kel=0
            far=1
            cel=0
        else: 
            kel=0
            far=1
            cel=0
        #print(kel)
        #print(far)
        #print(cel)
    
    #pushbutton 5 is clicked to display temperature in celsius     
    def on_pushButton5_clicked(self):#celsius is selected
        global kel
        global far
        global cel
        #print("celsius\n")
        self.labelscale.setText("Celsius")
        humidity,temperature = Adafruit_DHT.read(22,4)
        if temperature == None:
            #self.label_Temp1.setText("Not Connected")
            kel=0
            far=0
            cel=1
        else:
            #self.label_Temp1.setText(str(temperature)) 
            kel=0
            far=0
            cel=1
        #print(kel)
        #print(far)
        #print(cel)

app=QApplication(sys.argv)
widget=project()
widget.show()
sys.exit(app.exec_())




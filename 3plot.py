import csv
from itertools import takewhile    
from collections import deque
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
import os
import matplotlib.lines as mlines

CMD = r'"pscp -scp pi@fhlrasptemp.desy.de:/home/pi/sht21httpd-master/data.csv C:\Users\cordinge\Desktop\RaspberryPi_Sensor-master\3sensors\"' #Putty Command to copy the data from Pi to Windows 
fig = plt.figure(figsize=(7,6.5)) #Create the Window
ax1 = fig.add_subplot(1, 1, 1) #Define that only one Graph that takes up alle the Window size is displayed
ax2 = ax1.twinx() #Second Y-axis added to the Graph
fig.canvas.set_window_title('IR Chamber - Humidity and Temperature') #Winow Name
max_length = 20000 #Length of Arrays with len max_length    
small_length = 15 #Length
one_length = 1   #Length of 1 necessary for Alarm feature, most recent value displayed  

lasttime = deque(maxlen=one_length) #deque array instead of list due to better features
lasttemp = deque(maxlen=one_length)
lasthumid = deque(maxlen=one_length)


t = deque(maxlen=max_length) # time object
y = deque(maxlen=max_length) # temperature
h = deque(maxlen=max_length) # humidity

y2 = deque(maxlen=max_length) # temperature2
h2 = deque(maxlen=max_length) # humidity2

y3 = deque(maxlen=max_length) # temperature3
h3 = deque(maxlen=max_length) # humidity3

temp_avg = deque(maxlen=max_length)
humid_avg = deque(maxlen=max_length)

patch1 = mlines.Line2D([], [], color='red', marker = 's', label='Sensor 1: Temp') #Legend patches
patch2 = mlines.Line2D([], [], color='red', marker = 'o', label='Sensor 2: Temp')
patch3 = mlines.Line2D([], [], color='green', marker = 's', label='Sensor 1: Humidity')
patch4 = mlines.Line2D([], [], color='green', marker = 'o', label='Sensor 2: Humidity')
patch5 = mlines.Line2D([], [], color='red', marker = '^', label='Sensor 3: Temp')
patch6 = mlines.Line2D([], [], color='green', marker = '^', label='Sensor 3: Humidity')
patch7 = mlines.Line2D([], [], color='blue', marker = 'P', label='Average Temperature')
patch8 = mlines.Line2D([], [], color='blue', marker = '*', label='Average Humidity')

os.system(CMD)

def read_file(): #function that reads the csv and appends values to the deque arrays
    with open('data.csv', newline='') as f_input: #opens the file , comma delimiter default setting
        csv_input = csv.reader(f_input)
            #header = next(csv_input)        
    
        if len(t):
                list(takewhile(lambda row: datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S') != t[-1], csv_input)) #recognises time stamp
    
        for row in csv_input:
                
                t.append(datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')) #csv header useful, easy to declare what row in csv is what value
                y.append(float(row[0]))
                h.append(float(row[3]))
                y2.append(float(row[1]))
                h2.append(float(row[4]))
                y3.append(float(row[2]))
                h3.append(float(row[5]))
                

    
                lasttime.append(datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S'))
                lasttemp.append(float(row[0]))
                lasthumid.append(float(row[3]))
                
                avg_temp = (float(row[0])+float(row[1])+float(row[2]))/3 #for each iteration of the function read_file, an average value of each csv element of temp and humid
                avg_humid = (float(row[3])+float(row[4])+float(row[5]))/3 #is calculated and appended to a deque array which is plotted
                
                temp_avg.append(float(avg_temp))
                humid_avg.append(float(avg_humid))
                
def plot(): #plotting function
 
    

 avgtemp = ((sum(y)/len(y))+(sum(y2)/len(y2))+(sum(y3)/len(y3))/3) #for plt.title, displays avg values if no alarm is triggered
 avghumid = ((sum(h)/len(h))+(sum(h2)/len(h2))+(sum(h3)/len(h3))/3)
 
 last_time = list(lasttime)[-1] #necessary to convert deque element to something that can be recognised as a number or individual value
 last_temp = list(lasttemp)[-1]
 last_humid = list(lasthumid)[-1]
 last_temp2 = list(y2)[-1]
 last_humid2 = list(h2)[-1]
 last_temp3 = list(y3)[-1]
 last_humid3 = list(h3)[-1]


 ax1 = fig.add_subplot(1, 1, 1) #for some reason this is necessary for the plotting to look how it is supposed to look

 ax1.clear() #to avoid plotting over an existing plot, saves memory
 ax1.plot(t, y, 's-', color = 'r')
 ax1.plot(t, y2, 'o-', color = 'r')
 ax1.plot(t, y3, '^-', color = 'r')
 ax1.plot(t, temp_avg, 'P-', color = 'b')
 plt.yticks([0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40])
 ax1.set_ylabel('TEMPERATURE in C')
 ax1.set_xlabel('TIME')
 ax1.yaxis.label.set_color('red')
 plt.xticks(rotation=20)
 ax1.grid()
 ax1.tick_params(axis='y', colors='red')
 

 ax2.clear()
 ax2.plot(t, h, 's-', color = 'g')
 ax2.plot(t, h2, 'o-', color = 'g')
 ax2.plot(t, h3, '^-', color = 'g')
 ax2.plot(t, humid_avg, '*-', color = 'b')
 ax2.set_yticks([4,12,20,28,36,44,52,60,68,76,84,92,100])
 ax2.set_ylabel('HUMIDITY in %')
 ax2.yaxis.label.set_color('green')
 ax2.tick_params(axis='y', colors='green')

 ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m' + ' - ' + '%H:%M:%S')) #this recognises that the timestamp to be plotted on x-axis has to be changed
 plt.title('Average Temperature ' +  "%.2f" % avgtemp + '   ' + 'Average Humidity ' + "%.2f" % avghumid)
 fig.tight_layout() #resizes the window appropriately, even if you change the windows size


 if last_temp >= 20 and last_humid >= 25: #alarms, writes to log.csv
     plt.title('WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: ' + "%.2f" % last_temp + '/' + "%.2f" % last_temp2 + '/' + "%.2f" % last_temp3 + "   " + "%.2f" % last_humid + '/' + "%.2f" % last_humid2 + '/' + "%.2f" % last_humid3, color = 'r')
     print("WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: " + "%.2f" % last_temp + ' / ' + "%.2f" % last_humid + '  ' + str(last_time))

     myrow = str("WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: ") + str(lasttime) + ',' + str(lasttemp) + ',' + str(lasthumid) + '\n'
     fd = open('log.csv','a')
     fd.write(myrow)
     fd.close()


 elif last_temp >= 33:
    plt.title('WARNING! TEMPERATURE TOO HIGH: ' + "%.2f" % last_temp + '/' + "%.2f" % last_temp2 + '/' + "%.2f" % last_temp3, color = 'r')
    print("WARNING! TEMPERATURE TOO HIGH: " + "%.2f" % last_temp + '  ' + str(last_time))

    myrow = str("WARNING! TEMPERATURE TOO HIGH: ") + str(last_time) + ',' + str(last_temp) + '\n'
    fd = open('log.csv','a')
    fd.write(myrow)
    fd.close()

 elif last_humid >= 25:
    plt.title('WARNING! HUMIDITY TOO HIGH: ' + "%.2f" % last_humid + ' / ' + "%.2f" % last_humid2 + ' / ' + "%.2f" % last_humid3, color = 'r')
    print("WARNING! HUMIDITY TOO HIGH: " + str(last_humid) + '  ' + str(last_time))

    myrow = str("WARNING! HUMIDITY TOO HIGH: ") + str(last_time) + ',' + str(last_humid) + '\n'
    fd = open('log.csv','a')
    fd.write(myrow)
    fd.close()

 plt.legend(handles =[patch1, patch2, patch5, patch3, patch4, patch6, patch7, patch8]) #legend patches

def animate(i):
 read_file()
 plot()
 os.system(CMD) #the csv is copied from the Rpi every x seconds

 #fig.savefig('C:/Users/cordinge/Desktop/RaspberryPi_Sensor-master/plot.png', bbox_inches='tight', dpi=80)
 
 

    
ani = animation.FuncAnimation(fig, animate, interval=5000) #the function animate is called every x seconds, the window (fig) is a parameter that is necessary

#plt.show()


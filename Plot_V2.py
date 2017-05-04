from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
import os
from itertools import takewhile    
from collections import deque
from datetime import datetime
import csv
import time


fig = plt.figure(figsize=(7,6.5))
ax1 = fig.add_subplot(2, 1, 2)
ax2 = ax1.twinx()
ax3 = fig.add_subplot(2, 1, 1)
ax4 = ax3.twinx()
fig.canvas.set_window_title('IR Chamber - Humidity and Temperature')
max_length = 20000     # keep this many entries
small_length = 5
one_length = 1

t = deque(maxlen=max_length) # time object
y = deque(maxlen=max_length) # temperature
h = deque(maxlen=max_length) # humidity

tentime = deque(maxlen=small_length)
tentemp = deque(maxlen=small_length)
tenhumid = deque(maxlen=small_length)

lasttime = deque(maxlen=one_length)
lasttemp = deque(maxlen=one_length)
lasthumid = deque(maxlen=one_length)

CMD = r'"pscp -scp pi@fhlrasptemp.desy.de:/home/pi/pitemp/document.csv C:\Users\cordinge\Desktop\RaspberryPi_Sensor-master"'

def read_file():
    with open('document.csv', newline='') as f_input:
        csv_input = csv.reader(f_input)
        header = next(csv_input)        

        if len(t):
            list(takewhile(lambda row: datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S') != t[-1], csv_input))

        for row in csv_input:
            
            t.append(datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S'))
            y.append(float(row[1]))
            h.append(float(row[2]))

            tentime.append(datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S'))
            tentemp.append(float(row[1]))
            tenhumid.append(float(row[2]))

            lasttime.append(datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S'))
            lasttemp.append(float(row[1]))
            lasthumid.append(float(row[2]))


def plot():

 avgtemp = sum(y)/len(y)
 avghumid = sum(h)/len(h)
 
 
 last_temp = list(lasttemp)[-1]
 last_humid = list(lasthumid)[-1]
 last_time = list(lasttime)[-1]

 ax1 = fig.add_subplot(2, 1, 2)

 ax1.clear()
 ax1.plot(t, y, 'o', color = 'r')
 plt.yticks([16,18,20,22,24,26,28,30,32,34,36,38,40])
 ax1.set_ylabel('TEMPERATURE in C')
 ax1.set_xlabel('TIME')
 ax1.yaxis.label.set_color('red')
 plt.xticks(rotation=20)
 ax1.grid()
 ax1.tick_params(axis='y', colors='red')

 ax2.clear()
 ax2.plot(t, h, 'o', color = 'g') 
 ax2.set_yticks([4,12,20,28,36,44,52,60,68,76,84,92,100])
 ax2.set_ylabel('HUMIDITY in %')
 ax2.yaxis.label.set_color('green')
 ax2.tick_params(axis='y', colors='green')

 ax3.clear()
 ax3.plot(tentime, tentemp, 'o', color = 'r')
 ax3.set_yticks([18,20,22,24,26,28,30,32])
 ax3.set_ylabel('TEMPERATURE in C')
 ax3.yaxis.label.set_color('red')
 avgtentemp = sum(tentemp)/len(tentemp)
 avgtenhumid = sum(tenhumid)/len(tenhumid)
 ax3.set_title('Last Fifteen Minutes: ' + 'Temperature: ' + "%.2f" % avgtentemp + '  ' + 'Humidity: '  + "%.2f" % avgtenhumid)
 ax3.set_xlabel('TIME')
 ax3.grid()
 ax3.tick_params(axis='y', colors='red')

 ax4.clear()
 ax4.plot(tentime, tenhumid, 'o', color = 'g')
 ax4.set_yticks([16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50]) 
 ax4.set_ylabel('HUMIDITY in %')
 ax4.yaxis.label.set_color('green')
 ax4.tick_params(axis='y', colors='green')

 ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m' + ' - ' + '%H:%M:%S'))
 ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
 
 plt.title('Average Temperature ' +  "%.2f" % avgtemp + '   ' + 'Average Humidity ' + "%.2f" % avghumid)
 fig.tight_layout() 


 if last_temp >= 33 and last_humid >= 25:
     plt.title('WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: ' + "%.2f" % last_temp + ' / ' + "%.2f" % last_humid, color = 'r')
     print("WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: " + "%.2f" % last_temp + ' / ' + "%.2f" % last_humid + '  ' + str(last_time))

     myrow = str("WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: ") + str(lasttime) + ',' + str(lasttemp) + ',' + str(lasthumid) + '\n'
     fd = open('log.csv','a')
     fd.write(myrow)
     fd.close()


 elif last_temp >= 33:
    plt.title('WARNING! TEMPERATURE TOO HIGH: ' + "%.2f" % last_temp, color = 'r')
    print("WARNING! TEMPERATURE TOO HIGH: " + "%.2f" % last_temp + '  ' + str(last_time))

    myrow = str("WARNING! TEMPERATURE TOO HIGH: ") + str(last_time) + ',' + str(last_temp) + '\n'
    fd = open('log.csv','a')
    fd.write(myrow)
    fd.close()

 elif last_humid >= 25:
    plt.title('WARNING! HUMIDITY TOO HIGH: ' + str(last_humid), color = 'r')
    print("WARNING! HUMIDITY TOO HIGH: " + str(last_humid) + '  ' + str(last_time))

    myrow = str("WARNING! HUMIDITY TOO HIGH: ") + str(last_time) + ',' + str(last_humid) + '\n'
    fd = open('log.csv','a')
    fd.write(myrow)
    fd.close()

def animate(i):
 read_file()
 plot()
 os.system(CMD) 
 
 
ani = animation.FuncAnimation(fig, animate, interval=5000)

plt.show
'''
Author: Enzo Cording
'''

from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
import os

x = []	
y = []
t = []
h = []

fig = plt.figure(figsize=(7,6.5))
ax1 = fig.add_subplot(2, 1, 2)
ax2 = ax1.twinx()
ax3 = fig.add_subplot(2, 1, 1)
ax4 = ax3.twinx()
fig.canvas.set_window_title('IR Chamber - Humidity and Temperature')

CMD = r'"pscp -scp pi@fhlrasptemp.desy.de:/home/pi/pitemp/document.csv C:\Users\cordinge\Desktop\RaspberryPi_Sensor-master"'

def plot(i):
 
 readFile = open('document.csv', 'r')
 sepFile = readFile.read().split('\n')
 readFile.close()
 for idx, plotPair in enumerate(sepFile):
     if plotPair in '. ':
         # skip. or space
         continue
     if idx > 1:  # to skip the first line
         xAndY = plotPair.split(',')
         time_string = xAndY[0]
         time_string1 = datetime.strptime(time_string, '%d/%m/%Y %H:%M:%S')
      
         t.append(time_string1)
         y.append(float(xAndY[1]))
         h.append(float(xAndY[2]))
        
 avgtemp = sum(y)/len(y)
 avghumid = sum(h)/len(h)
 
 tentime = t[-60:]
 tentemp = y[-60:]
 tenhumid = h[-60:] 

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
 ax3.set_title('Last Five Minutes: ' + 'Temperature: ' + "%.2f" % avgtentemp + '  ' + 'Humidity: '  + "%.2f" % avgtenhumid)
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

 lasttemp = y[-1]
 lasthumid = h[-1]
 lasttime = t[-1]
 
 if(lasttemp >= 33 and lasthumid >= 25):
     plt.title('WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: ' + "%.2f" % lasttemp + ' / ' + "%.2f" % lasthumid, color = 'r')
     print("WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: " + "%.2f" % lasttemp + ' / ' + "%.2f" % lasthumid + '  ' + str(lasttime))

     myrow = str("WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: ") + str(lasttime) + ',' + str(lasttemp) + ',' + str(lasthumid) + '\n'
     fd = open('log.csv','a')
     fd.write(myrow)
     fd.close()


 elif(lasttemp >= 33):
    plt.title('WARNING! TEMPERATURE TOO HIGH: ' + "%.2f" % lasttemp, color = 'r')
    print("WARNING! TEMPERATURE TOO HIGH: " + "%.2f" % lasttemp + '  ' + str(lasttime))

    myrow = str("WARNING! TEMPERATURE TOO HIGH: ") + str(lasttime) + ',' + str(lasttemp) + '\n'
    fd = open('log.csv','a')
    fd.write(myrow)
    fd.close()

 elif(lasthumid >= 25):
    plt.title('WARNING! HUMIDITY TOO HIGH: ' + "%.2f" % lasthumid, color = 'r')
    print("WARNING! HUMIDITY TOO HIGH: " + "%.2f" % lasthumid + '  ' + str(lasttime))

    myrow = str("WARNING! HUMIDITY TOO HIGH: ") + str(lasttime) + ',' + str(lasthumid) + '\n'
    fd = open('log.csv','a')
    fd.write(myrow)
    fd.close()
   
 #os.remove('C:/Users/cordinge/Desktop/RaspberryPi_Sensor-master/plot.png')  
 #fig.savefig('C:/Users/cordinge/Desktop/RaspberryPi_Sensor-master/plot.png', bbox_inches='tight', dpi=80)   
 
 
 fig.tight_layout()  
 

 os.system(CMD)
''' 
 if (response != 1):
      print('hi')
      os.system(CMD)
     
 if response != 1:
      print("Raspberry is currently offline... Exiting Program...")
      time.sleep(5)
      exit()
'''
 


ani = animation.FuncAnimation(fig, plot, interval=5000)

plt.plot()

    


   
   





#if (event.key == pygame.K_t):
#plt.title('CURRENT TEMPERATURE: ' + "%.2f" % lasttemp, color = 'g')

#elif (event.key == pygame.K_p):
#plt.title('CURRENT PRESSURE: ' + "%.2f" % lastpress, color = 'g')


'''
 if(avgtemp >= 27 and avgpress >= 1016):
	plt.title('WARNING! BOTH AVERAGE TEMP AND PRESS TOO HIGH: ' + "%.2f" % avgtemp + ' / ' + "%.2f" % avgpress, color = 'r')

 elif(avgtemp >= 27):
	plt.title('WARNING! AVERAGE TEMPERATURE TOO HIGH: ' + "%.2f" % avgtemp, color = 'r')

 elif(avgpress >= 1016):
	plt.title('WARNING! AVERAGE PRESSURE TOO HIGH: ' + "%.2f" % avgpress, color = 'r')
'''

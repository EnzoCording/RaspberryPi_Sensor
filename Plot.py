from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import matplotlib.animation as animation
import matplotlib.patches as mpatches


x = []	
y = []
time = []
h = []

fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(2, 1, 2)
ax2 = ax1.twinx()
ax3 = fig.add_subplot(2, 1, 1)
ax4 = ax3.twinx()

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
         #print(time_string1)
	 time.append(time_string1)
         y.append(float(xAndY[1]))
	 h.append(float(xAndY[2]))
  	

 avgtemp = sum(y)/len(y)
 avghumid = sum(h)/len(h)
 

 tentime = time[-60:]
 tentemp = y[-60:]
 tenhumid = h[-60:] 

 ax1 = fig.add_subplot(2, 1, 2)


 ax1.clear()
 ax1.plot(time, y, 'o', color = 'r')
 plt.yticks([16,18,20,22,24,26,28,30,32,34,36,38,40])
 ax1.set_ylabel('TEMPERATURE')
 ax1.set_xlabel('TIME')
 ax1.yaxis.label.set_color('red')
 plt.xticks(rotation=80)
 ax1.grid()


 ax2.clear()
 ax2.plot(time, h, 'o', color = 'g') 
 ax2.set_yticks([0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100])
 ax2.set_ylabel('HUMIDITY')
 ax2.yaxis.label.set_color('green')


 ax3.clear()
 ax3.plot(tentime, tentemp, 'o', color = 'r')
 ax3.set_yticks([16,18,20,22,24,26,28,30,32,34,36,38,40])
 ax3.set_ylabel('TEMPERATURE')
 ax3.yaxis.label.set_color('red')
 avgtentemp = sum(tentemp)/len(tentemp)
 avgtenhumid = sum(tenhumid)/len(tenhumid)
 ax3.set_title('Last Five Minutes: ' + "%.2f" % avgtentemp+ ' / ' + "%.2f" % avgtenhumid)
 ax3.set_xlabel('TIME')
 ax3.grid()


 ax4.clear()
 ax4.plot(tentime, tenhumid, 'o', color = 'g')
 ax4.set_yticks([16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]) 
 ax4.set_ylabel('HUMIDITY')
 ax4.yaxis.label.set_color('green')




 
 ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M:%S'))

 ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
 #fig.autofmt_xdate(rotation=45)
 
 fig.tight_layout() 
 plt.title('Average Temperature ' +  "%.2f" % avgtemp + '   ' + 'Average Humidity ' + "%.2f" % avghumid)

 lasttemp = y[-1]
 lasthumid = h[-1]
 lasttime = time[-1]
 
 if(lasttemp >= 33 and lasthumid >= 25):
	plt.title('WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: ' + "%.2f" % lasttemp + ' / ' + "%.2f" % lasthumid, color = 'r')
	print("WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: " + "%.2f" % lasttemp + ' / ' + "%.2f" % lasthumid + '  ' + str(lasttime))


 elif(lasttemp >= 33):
	plt.title('WARNING! TEMPERATURE TOO HIGH: ' + "%.2f" % lasttemp, color = 'r')
	print("WARNING! TEMPERATURE TOO HIGH: " + "%.2f" % lasttemp + '  ' + str(lasttime))

 elif(lasthumid >= 25):
	plt.title('WARNING! HUMIDITY TOO HIGH: ' + "%.2f" % lasthumid, color = 'r')
	print("WARNING! HUMIDITY TOO HIGH: " + "%.2f" % lasthumid + '  ' + str(lasttime))

 
ani = animation.FuncAnimation(fig, plot, interval=5000)


plt.show()







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
 





























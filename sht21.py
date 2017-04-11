#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Importing libraries
import time
import rpi_i2c
import os
import sys


# Creating the class sht21
class sht21:

    i2c = rpi_i2c.I2C()                                       # I2C Wrapper Class (recall the class)

# Complete measurement function
    def measure(self, dev=1, scl=3, sda=2):
        self.open(dev, scl, sda)                              # Open the device
        t = self.read_temperature()                           # Get temperature
        rh = self.read_humidity()                             # Get humidity
        self.i2c.close()                                      # Close the device
        return (t, rh)

# Open and initialise the I2C port in the raspberry
    def open(self, dev=1, scl=3, sda=2):
        self.i2c.open(0x40,dev, scl, sda)                     # Open the port of the device and set the the clock and data wire
        self.i2c.write([0xFE])                                # Execute Softreset Command  (default T=14Bit RH=12)
        time.sleep(0.050)

# Temperature measurement function
    def read_temperature(self):
        self.i2c.write([0xF3])                                # Trigger T measurement (no hold master)
        time.sleep(0.066)                                     # Waiting time, typ=66ms, max=85ms @ 14Bit resolution
        data = self.i2c.read(3)
        if (self._check_crc(data, 2)):
            t = ((data[0] << 8) + data[1]) & 0xFFFC           # Set status bits to zero
            t = -46.82 + ((t * 175.72) / 65536)               # T = 46.82 + (175.72 * ST/2^16 )
            return round(t, 1)
        else:
            return None

# Humidity measurement function
    def read_humidity(self):
        self.i2c.write([0xF5])                                # Trigger RH measurement (no hold master)
        time.sleep(0.25)                                      # Waiting time, typ=22ms, max=29ms @ 12Bit resolution
        data = self.i2c.read(3)
        if (self._check_crc(data, 2)):
            rh = ((data[0] << 8) + data[1]) & 0xFFFC          # Set status bits to zero
            rh = -6 + ((125 * rh) / 65536)
            if (rh > 100): rh = 100
            return round(rh, 1)
        else:
            return None

# Close function (closes the i2c connection)
    def close(self):
        self.i2c.close()

# Checksum function (standar function in order to know when some error appear)
    def _check_crc(self, data, length):
        
        #Calculates checksum for n bytes of data and compares it with expected
        crc = 0
        for i in range(length):
            crc ^= (ord(chr(data[i])))
            for bit in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x131                   # CRC POLYNOMIAL
                else:
                    crc = (crc << 1)
        return True if (crc == data[length]) else False

# Taking data
if __name__ == "__main__":
    SHT21 = sht21()
    while True:

        (t0, rh0) = SHT21.measure(None,3,2)  # Use GPIOs SCL=3, SDA=2
        #(t1, rh1) = SHT21.measure(None,3,2)  # Use GPIOs SCL=3, SDA=2
        #print("%s°C\t%s%%\t%s°C\t%s%%" % (t0,rh0,t1,rh1))
        #print("%s°C\t%s%%" % (t0,rh0))
	if(t0==None or rh0==None):
		continue
	current_time = time.strftime("%d/%m/%Y %H:%M:%S")
    	print (current_time, "Temperature: ", t0 ,"   Humidity: ", rh0)
   	myrow = str(current_time) + ',' + str(t0) + ',' + str(rh0) + '\n'

 	fd = open('document.csv','a')
	fd.write(myrow)
   	fd.close()
      	os.system("scp document.csv enzo@atlaswin10:/home/enzo/Programs/")
 
        #time.sleep(0.3)	
        #  except:
        #    print("sht21 I/O Error")
        #   break
        time.sleep(5)	

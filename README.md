# RaspberryPi_Sensor
Uses Matplotlib and LabView to Plot a live updating graph using the SHT21 sensor


You need:


Raspberry Pi with:
  
      Python 2.7
  
      SHT-21 Sensor
  
      document.csv
  
      rpi_i2c.py
  
      sht21.py
  
Computer with:
  
      Plot.py
  
      RSA ssh connection to and from the Pi
  
     --> as it copies the document.csv file to the pc
  
     Matplotlib
  
      Python 2.7
  
Execute as follows:
Open Putty, load pi session and connect without a password (rsa established)
Then:
    $cd RPi_Htp
    $cd BMP180
    $cd Python
    $python sht21.py

On The Laptop, run Python with Spyder (Anaconda 3)
Then Open irmonitor.vi in LabView and you will have the Python Programm embedded into the Labview vi

# RaspberryPi_Sensor
Uses Matplotlib to Plot a live updating graph using the SHT21 sensor
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
  
  On the RPi:
    $ python sht21.py
    
  On the Pc:
    $ python Plot.py

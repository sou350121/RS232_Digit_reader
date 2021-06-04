# -*- coding: utf-8 -*-

import serial
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
import base64

# configure the serial connections (the parameters differs \
# on the device you are connecting to)
ser = serial.Serial(
    port='COM3',    # input your port name as string
    baudrate=9600,
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
ser.isOpen()
# Reading the data from the serial port. This will be running in an infinite loop.

# setup the window for visualization
#plot_window = 20
#y_var = np.array(np.zeros([plot_window]))
#
#plt.ion()
#fig, ax = plt.subplots()
#line, = ax.plot(y_var)
#

while True :
#    try:
    # get keyboard input
    bytesToRead = ser.inWaiting()
    data = ser.read(bytesToRead)
#    decoded_bytes = data[0:len(data)-2].decode("utf-8")
    # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    
    time.sleep(1)
#    print(data)
#    print(decoded_bytes)
    data_decoded_list = data.decode("UTF-8").split()
    Z_list = [element.split(',')[0] for element in data_decoded_list]
    print(data.decode("UTF8"))
    # write the data on .csv
    with open("test_data.csv","a") as f:
        writer = csv.writer(f,delimiter=",")
        [writer.writerow([time.time(),Z]) for Z in Z_list]
#        writer.writerow([time.time(),data_decoded])
    
#    y_var = np.append(y_var,data_decoded)
#    y_var = y_var[1:plot_window+1]
#    line.set_ydata(y_var)
#    ax.relim()
#    ax.autoscale_view()
#    fig.canvas.draw()
#    fig.canvas.flush_events()    
    
#    except:
#        print("except")
#    else:
#        print("done!")
#    finally:
#        ser.close() 

'''

while True:
    try:
        ser_bytes = ser.readline()
        try:
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            print(decoded_bytes)
        except:
            continue
        with open("test_data.csv","a") as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow([time.time(),decoded_bytes])
        y_var = np.append(y_var,decoded_bytes)
        y_var = y_var[1:plot_window+1]
        line.set_ydata(y_var)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        print("Keyboard Interrupt")
        break
'''
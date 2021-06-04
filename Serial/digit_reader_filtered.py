# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 21:15:20 2021

@author: mn
"""

# -*- coding: utf-8 -*-

import time
from  datetime import datetime
import serial  # Rs232
import base64
import csv

import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy import signal, misc # singal processing

# configure the serial connections (the parameters differs \
# on the device you are connecting to)
ser = serial.Serial(
    port='COM5',    # input your port name as string
    baudrate=9600,
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
ser.isOpen()

columns=["time", "Z", "theta", "other"]
df = pd.DataFrame(columns=columns)

# fig, ax = plt.subplots()
# ax.axis([0, 100, 30000,120000])
# plt.axis([0,100,30000,120000])

plt.ion()
plt.show()


# fig.canvas.manager.show()
# y = np.random.rand(10)*10000
# lines = ax.plot(y)

f = plt.figure()

# define the initial time
now = datetime.now()
time_int = now.strftime("%m%d%H%M")

#with open("test_data{0}.csv".format(time_int),"w") as csvf:
 #   writer = csv.writer(csvf,delimiter=",")

def float_str(string):
    try:
        return float(string)
    except:
        return -1
    
def Bspline_filter(singal):
    try:
        return signal.sosfilt(singal, x)
    except: 
        return -1

def Butter_filter(singal):
    try:
        sos = signal.butter(5, 0.05,output='sos')#an order 3 lowpass butterworth filter
        return signal.sosfiltfilt(sos,singal)
    except: 
        return []

def SNR(signal, axis=0, ddof=0):
    try:
        # signal = np.asanyarray(signal) Convert the input to an ndarray, but pass ndarray subclasses through.
        m = signal.mean(axis)
        sd = signal.std(axis=axis, ddof=ddof)
        return np.where(sd == 0, 0, m/sd)  #numpy.where(condition[, x, y]) Return elements chosen from x or y depending on condition.
    except: 
        return []

# Reading the data from the serial port. This will be running in an infinite loop.#
while True :

    # get keyboard input
    bytesToRead = ser.inWaiting()
    data = ser.read(bytesToRead)
    # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    # if len(data) < 5:
    #     continue


    # time.sleep(1)

    # print(data.decode("UTF8"))

    data_decoded_list = data.decode("UTF-8")
    # data_list = [element.split(',') for element in data_decoded_list]

    # split data into lines
    data_lst = data_decoded_list.split("\n")


    # convert data into a list of each elements
    data_items = [line.split(",") for line in data_lst]
    # data_lst = [float(i) for i in data_lst]

    data_items = [line for line in data_items if len(line) == 3]
    
    time_label = datetime.now().strftime("%M%S%f")

    # generate current timestamp
    [line.insert(0, datetime.now().strftime("%M%S%f")) for line in data_items]


    data_items = [dict(zip(columns, line)) for line in data_items if float_str(line[1]) != -1 and float_str(line[1]) > 30000 and float_str(line[1]) < 120000]
    #print(data_items)

    df = df.append(data_items, ignore_index=True)
    df = df.dropna()
    df.to_excel("data.xlsx")

    df[["Z"]] = df[["Z"]].astype(float)
    y = df[["Z"]].to_numpy().reshape(-1)
    t = df[['time']].to_numpy().reshape(-1)
    #y_filter = signal.cspline1d_eval(signal.cspline1d(y),t.astype(float))
    y_filter = Butter_filter(y)
    #y_SNR = SNR(y)
    #length = np.lin
    print(y_filter)
    x = range(y.shape[0])
    # print(y)
    # lines[0].set_ydata(y)
    # fig.canvas.draw()
    # fig.canvas.flush_events()
    f.clear()
    plt.plot(x[-1000:], y[-1000:],label='ori',color='b')
    if len(y_filter) != 0 : 
        plt.plot(x[-1000:], y_filter[-1000:],label='butterFil',color= 'k')
    #if len(y_SNR) != 0 : 
      #  plt.plot(x[-1000:], y_filter[-1000:],label='SNR',color= 'r')
    plt.draw()

    plt.pause(0.001)

    time.sleep(1)
    
    

    #write the data on .csv
    
    with open("test_data{0}.csv".format(time_int),"w",newline='') as csvf:
        writer = csv.writer(csvf,delimiter=",")
        if len(y)  == 0 : continue
        [writer.writerow([tt,yy,yf]) for tt,yy,yf in zip(t,y,y_filter)]
   
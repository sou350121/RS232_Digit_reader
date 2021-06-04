# -*- coding: utf-8 -*-

import time
from  datetime import datetime
import serial
import base64
import csv

import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

    print(data_items)

    data_items = [line for line in data_items if len(line) == 3]

    # generate current timestamp
    [line.insert(0, datetime.now().strftime("%d%H%M%S%f")) for line in data_items]

    print(data_items)

    data_items = [dict(zip(columns, line)) for line in data_items if float_str(line[1]) != -1 and float_str(line[1]) > 30000 and float_str(line[1]) < 120000]
    print(data_items)

    
    df = df.append(data_items, ignore_index=True)
    df = df.dropna()
    df.to_excel("data.xlsx")

    df[["Z"]] = df[["Z"]].astype(float)
    y = df[["Z"]].to_numpy().reshape(-1)
    x = range(y.shape[0])
    # print(y)
    # lines[0].set_ydata(y)
    # fig.canvas.draw()
    # fig.canvas.flush_events()
    f.clear()
    plt.plot(x[-1000:], y[-1000:])
    plt.draw()

    plt.pause(0.001)

    time.sleep(1)

    #write the data on .csv
    with open("test_data{0}.csv".format(time_int),"w",newline='') as csvf:
        writer = csv.writer(csvf,delimiter=",")
        [writer.writerow([time.time(),Z]) for Z in y]
   
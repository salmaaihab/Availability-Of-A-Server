import os
import time
import socket
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import datetime

# from google.colab.patches import cv2_imshow


url = input("Enter domain URL: ")
totalTime = float(input("Please enter the total time for running the code in hours"))

flag = 0
present = 0
running_time = 0
max_time = totalTime * 60 * 60  # 8 hours in seconds
downtime = 0
timeNow = 0
timeDownBefore = 0
ip_address = " "
down_start_time = 0
last_response_time = None
mtd = 0
availability = 0
var = 0

totalcounts=0
successcounts=0

# name of csv file
filename = "availability_records.csv"

try:
    ip_address = socket.gethostbyname(url)
    print(f"IP address of {url}: {ip_address}")
    present = 1

except socket.gaierror:
    print(f"{url} is not a valid domain name")

if present == 1:
    timestamps = []
    availability_values = []
    start_time = time.time()
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        while running_time < max_time:
            response = os.system("ping -n 1 " + ip_address)

            if response == 0:
                print(ip_address, "is reachable")
                successcounts = successcounts + 1
                var = 1
                print(var)
                # if reachable , iwant to calculate was it previously down to calculate the downtime
                if down_start_time > 0:
                    duration = time.time() - down_start_time
                    downtime += duration
                    down_start_time = 0
                    print(f"Downtime ended: {duration:.2f} seconds")
                last_response_time = time.time()
            else:
                print(ip_address, "is not reachable")
                var = 0

                print("Time Now when it is down ")
                timeNow = time.time()
                print(timeNow)
                if down_start_time == 0:
                    down_start_time = time.time()
                    print(f"Downtime started at {down_start_time}")
            print("Code is still running...")
            # Update the running time
            running_time = time.time() - start_time
            print(running_time)
            print(max_time)

            # Wait for a bit before checking the time again
            csvwriter.writerow([str(time.time()), str(var)])
            timestamps.append(time.time())
            availability_values.append(var)
            totalcounts = totalcounts +1
            time.sleep(3)

    #print("Code has been running for " + str(totalTime) + " hours. Stopping now.")

    length = len(timestamps)
    lengthcol = length / 2
    print(str(lengthcol))
    i = 0

    while i < lengthcol:
        if availability_values[i] == 1:
            print("sssss")
        i = i + 1




    if down_start_time > 0:
        duration = time.time() - down_start_time
        downtime = downtime + duration - 3
        print(f"Downtime ended: {duration:.2f} seconds")
        print(f"Total downtime: {downtime:.2f} seconds")


    #availability = (max_time - downtime) / max_time

    #if downtime > totalTime:
    #   availability = 0
    availability = successcounts/totalcounts
    print(successcounts)
    print(totalcounts)
    percentage = availability * 100

    print(" Your system's availability metrics is " + str(availability))
    print(" Your system's availability metrics is " + str(percentage) + "% ")


    csvfile.close()
    data = pd.read_csv('availability_records.csv')
    data
    ###graph printing
    x = []
    y = []

    with open('availability_records.csv', 'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            if len(row) >= 2:  # Check if the row has at least 2 elements
                x.append(float(row[0]))  # Convert to float
                y.append((row[1]))  # Convert to int

    timestamps = [datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S') for ts in timestamps]

    plt.plot(timestamps, availability_values)
    plt.ylabel('Availability')
    plt.xlabel('Time')
    plt.title('Server Availability ', fontsize=20)
    plt.grid(True)
    plt.yticks([0, 1])
    plt.xticks(rotation=45)
    plt.show()

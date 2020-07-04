import tkinter
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import csv

data = []

window = tkinter.Tk()
top = Frame(window)
bottom = Frame(window)
top.pack(side=TOP)
bottom.pack(side=BOTTOM)

# doing the formatting of str to datetime and formatting the DataFrame for calculations
df = pd.read_csv("database.csv", delimiter=",")
df["time_start"] = pd.to_datetime(df.time_start, format="%H:%M:%S")
df["time_end"] = pd.to_datetime(df.time_end, format="%H:%M:%S")
df["time_coded"] = df["time_end"] - df["time_start"]
print(df)
grouped = df[["date", "time_coded"]].groupby("date").sum()
#grouped = df.groupby(df["date"])["time_coded"].sum()
print(grouped)
# plotting the values
#plt.plot(grouped, linewidth = 2, color = "darkgreen", markersize = 12)
fig = plt.Figure(figsize=(9, 7), dpi=100)
#ax = fig.add_subplot(111).plot(grouped)
ax = fig.add_subplot(111)
bar = FigureCanvasTkAgg(fig, window)
bar.get_tk_widget().pack(in_=top, fill=BOTH, expand=True, pady=10)
#plt.plot(grouped, linewidth=2, color="darkgreen", markersize=12)
grouped.plot(kind="line", ax=ax)
ax.set_title("Time spent coding")
ax.set_xlabel("Day")
ax.set_ylabel("Time in Hours")

def start_timer():
    begin = datetime.datetime.now()
    data.append(begin.strftime("%d-%m-%Y"))
    data.append(begin.strftime("%H:%M:%S"))

def end_timer():
    ending = datetime.datetime.now()
    data.append(ending.strftime("%H:%M:%S"))

    def data_collection(info):
        with open("database.csv", "a", newline="") as database:
            write = csv.writer(database, delimiter=",")
            write.writerows([info])
            data.clear()
            return database

    return data_collection(data)


btn_start = Button(window, text="Start", fg="black", font=("Segoe UI", 20), command=start_timer,
                   activebackground="grey", width=10)
btn_start.pack(in_=bottom, side=LEFT, pady=20, padx=10)
btn_end = Button(window, text="End", fg="black", font=("Segoe UI", 20), command=end_timer, activebackground="grey",
                 width=10)
btn_end.pack(in_=bottom, side=LEFT, pady=20, padx=10)
window.title("Coding Tracker")
window.geometry("800x800+10+20")
window.mainloop()

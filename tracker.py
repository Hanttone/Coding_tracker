import tkinter
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import csv


data = []

#GUI button and graph placing
window = tkinter.Tk()
top = Frame(window)
bottom = Frame(window)
top.pack(side=TOP)
bottom.pack(side=BOTTOM)

def start_graph():
    #formatting to datetime and creating dataframe with hours/minutes in float
    df = pd.read_csv("database.csv", delimiter=",")
    df["time_start"] = pd.to_datetime(df.time_start, format="%H:%M")
    df["time_end"] = pd.to_datetime(df.time_end, format="%H:%M")
    df["time_coded_h"] = df["time_end"].dt.hour - df["time_start"].dt.hour
    df["time_coded_m"] = df["time_end"].dt.minute - df["time_start"].dt.minute
    df["minutes"] = round(df["time_coded_m"]/60, 2)
    df["coded_float"] = df["time_coded_h"].astype(float) + df["minutes"]
    grouped = df[["date", "coded_float"]].groupby("date").sum()

    #plotting values
    fig = plt.Figure(figsize=(15, 7), dpi=100)
    ax = fig.add_subplot(111)
    bar = FigureCanvasTkAgg(fig, window)
    bar.get_tk_widget().pack(in_=top, fill=BOTH, expand=True, pady=10)
    grouped.plot(kind="line", ax=ax, color="green")
    ax.set_title("Time spent coding")
    ax.set_xlabel("Day")
    ax.set_ylabel("Time in Hours")
    ax.get_legend().remove()

def refresh_graph():
    return start_graph()

def start_timer():
    begin = datetime.datetime.now()
    data.append(begin.strftime("%d-%m-%Y"))
    data.append(begin.strftime("%H:%M"))
    btn_start.bind('<Button-1>')
    btn_start.config(relief='sunken')

def end_timer():
    ending = datetime.datetime.now()
    data.append(ending.strftime("%H:%M"))
    btn_end.bind('<Button-1>')
    btn_start.config(relief='raised')

    def data_collection(info):
        with open("database.csv", "a", newline="") as database:
            write = csv.writer(database, delimiter=",")
            write.writerows([info])
            data.clear()
            return database
    return data_collection(data)

#button definitions and actions
btn_start = Button(window, text="Start", fg="black", font=("Segoe UI", 20), command=start_timer,
                   activebackground="grey", width=15)
btn_start.pack(in_=bottom, side=LEFT, pady=20, padx=10)
btn_end = Button(window, text="End", fg="black", font=("Segoe UI", 20), command=end_timer, activebackground="grey",
                 width=15)
btn_end.pack(in_=bottom, side=LEFT, pady=20, padx=10)
btn_refresh = Button(window, text="Refresh graph", fg="black", font=("Segoe UI", 20), command=refresh_graph, activebackground="grey",
                 width=15)
btn_refresh.pack(in_=bottom, side=LEFT, pady=20, padx=10)

#initializing app
start_graph()
window.title("Coding Tracker")
window.geometry("1000x800+0+0")
window.mainloop()

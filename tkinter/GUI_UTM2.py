######################## Underwater Trenching Mechine GUI #########################
# Author : Asri Gania
# Date   : August 1st 2019
###################################################################################

from tkinter import *

disp = Tk()

#---------------------------------------------------------------------------------

#import tkinter
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (
	FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import style


style.use('fivethirtyeight')

fig = Figure(figsize=(6,3), dpi=80) #
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

#ax1 = plt.subplot2grid((6,1), (0,0), rowspan=1, colspan=1)
#ax2 = plt.subplot2grid((6,1), (1,0), rowspan=4, colspan=1)
#ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1)

#---------------------------------------------------------------------------------

import time
import paho.mqtt.client as paho
broker="192.168.1.18"
port=1883

print ("ini percoban")

# Photo
#gambar=PhotoImage(file="safe_image.gif")
#Label(disp, image=gambar, bg="black").grid(row=0, column=0, sticky=E)
t_btn_on = PhotoImage(file="toggleon.png")
t_btn_off = PhotoImage(file="toggleoff.png")
btn_on=t_btn_on.subsample(2,2)
btn_off=t_btn_off.subsample(2,2)

var=DoubleVar()


#========= 1. Fungsi-fungsi:

def create_plots():
    xs = []
    ys = []

    for i in range(10):
        x = i
        y = random.randrange(10)

        xs.append(x)
        ys.append(y)
    return xs, ys

def animate(i):
	x,y = create_plots()
	ax1.clear()
	ax2.clear()
	ax1.plot(x,y)
	ax2.plot(x,y)

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

def blade_Vpos():
	#print ("niali sedang dikirim :" + str (var.get()))
	print (var.get())

def captor_stat1():
	Button(disp, image=btn_on, command=captor_stat2).place(relx=0.7, rely=0.15)
def captor_stat2():
	Button(disp, image=btn_off, command=captor_stat1).place(relx=0.7, rely=0.15)
def motor1_stat1():
	Button(disp, image=btn_on, command=motor_stat2).place(relx=0.7, rely=0.15)
def motor1_stat2():
	Button(disp, image=btn_off, command=motor_stat1).place(relx=0.7, rely=0.15)
def motor2_stat1():
	Button(disp, image=btn_on, command=motor_stat2).place(relx=0.7, rely=0.15)
def motor2_stat2():
	Button(disp, image=btn_off, command=motor_stat1).place(relx=0.7, rely=0.15)

def close_window():
		disp.quit()
		disp.destroy()
		exit()

#========== 2. MAIN :

def main():

	disp.title("Underwater Trenching Machine GUI")
	disp.minsize(width=1020, height=600)
	disp.maxsize(width=1080, height=720)
	#disp.configure(background="blue")

	# label
	Label (disp, text="UNDERWATER TRENCHING MACHINE INTERFACE", bg="black", fg="White", font="none 12 bold").pack(anchor=CENTER)
	

	
	
	# video streaming
	##video_out = Text(disp, width=100, height=30, wrap=WORD, background="black").place(relx=0.0,rely=0.15)
	#Label (disp, text="video streaming").place(relx=0.0,rely=0.15)

	#grafik
	canvas = FigureCanvasTkAgg(fig, master=disp)  # A tk.DrawingArea.
	canvas.draw()
	canvas.get_tk_widget().place(relx=0.1,rely=0.15)#pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
	Label(disp, text="I. Kedalaman").place(relx = 0.2, rely= 0.58)
	Label(disp, text="II. Tekanan").place(relx = 0.4, rely= 0.58)

	#toolbar = NavigationToolbar2Tk(canvas, disp)
	#toolbar.update()
	#canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


	#canvas.mpl_connect("key_press_event", on_key_press)

	# widget
	blade_slider = Scale(disp, from_=0, to=1024, width=50, length=350, sliderlength=50, variable=var, command=blade_Vpos).place(relx=0.8,rely=0.15) #tickinterval
	#captor_btn   = Button(disp, text="OFF", width=3, height=3, command=captor_stat).place(relx=0.8,rely=0.3)
	Button(disp, image=btn_off, command=captor_stat1).place(relx=0.7, rely=0.15)
	#Button(disp, image=btn_on, command=captor_stat).place(relx=0.7, rely=0.3)
	Label(disp, text="Pencapit").place(relx = 0.73, rely= 0.25)
	Button(disp, image=btn_off, command=motor1_stat1).place(relx=0.7, rely=0.35)
	Label(disp, text="Motor 1").place(relx = 0.73, rely= 0.45)
	Button(disp, image=btn_off, command=motor2_stat1).place(relx=0.7, rely=0.55)
	Label(disp, text="Motor 2").place(relx = 0.73, rely= 0.65)

	#canvas
	#canvas=Canvas(disp, width=500, height=500)
	#canvas.place(x=0, y=0)

	#canvas.create_line(0,0,200,50, fill="yellow")	

	

		

	# closing the window
	Button(disp, text="CLOSE", width=3, command=close_window).pack(anchor=CENTER)
	
	#live grafik
	ani = animation.FuncAnimation(fig, animate, interval=1000)

	# run the mainloop
	disp.mainloop() #mainloop

if __name__ == '__main__':
    main()

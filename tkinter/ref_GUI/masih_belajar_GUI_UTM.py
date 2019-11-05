######################## Underwater Trenching Mechine GUI #########################
# Author : Asri Gania
# Date   : August 1st 2019
###################################################################################

from tkinter import *

disp = Tk() #deklarasikan?????

print ("ini percoban")

#========= 1. Fungsi-fungsi:

#var=DoubleVar()
def blade_Vpos():
	#kirim nilai blade
	Vpos_val = 1#str(var.get())
	print ("niali sedang dikirim :"); print (str(Vpos_val))

#hitung=0
status_btn="OFF"
def klik_ON():
	status_btn="ON"
def klik_OFF():
	status_btn="OFF"
def captor_stat():
	if (status_btn=="OFF"):
		print ("capit mencapit")
		Button(disp, text="OFF", width=3, height=3, command=klik_ON).grid(row=0,column=1)
		status_btn="ON"
		print (status_btn)
	elif (status_btn=="ON"):
		print ("capit terbuka")
		Button(disp, text="ON", width=3, height=3, command=klik_OFF).grid(row=0,column=1)
		status_btn="OFF"
		print (status_btn)
	#kirim satatus capit
	#hitung+=1
	#while hitung==1:
		
	#print ('capit terbuka')

def click():
	mengambil_teks_yang_diinput=textentry.get() #get()nya error #gara2 bukan piton 3 -_- #TEUING AH
	disp_out.delete(0.0, END)
	try: ### istilah baru
		isikan = login_dict[mengambil_teks_yang_diinput]
	except:
		isikan = " kata tidak terdaftar "
	disp_out.insert(END, isikan)

def close_window():
		disp.destroy()
		exit()

#========== 2. MAIN :

#-#def main():

disp.title("Underwater Trenching Mechine GUI")
disp.minsize(width=600, height=600)
disp.maxsize(width=1080, height=720)
	#disp.configure(background="blue")
	
	# Photo
	#gambar=PhotoImage(file="safe_image.gif")
	#Label(disp, image=gambar, bg="black").grid(row=0, column=0, sticky=E)

	# 1. label
Label (disp, text="UNDERWATER TRENCHING MECHINE", bg="black", fg="White", font="none 12 bold").grid(row=0, column=0, sticky=W)
Label (disp, text="CONTROL AND MONITORING", bg="black", fg="White", font="none 12 bold").grid(row=1, column=0, sticky=W)

	#label = Label (disp)
	#label.pack()
	# 2. text entry box
textentry = Entry(disp, width=20, bg="white").grid(row=2, column=0, sticky=W)
	# 3. button:

blade_slider = Scale(disp, from_=0, to=1024, width=50, command=blade_Vpos).grid(row=0,column=1)
	#blade_slider.pack()
	#blade_btn    = Button(disp, text="ON", width=3, height=3, command=blade_Vpos).grid(row=0,column=0) #kalau pakai pack() ini dikomen
	#blade_btn.pack()
captor_btn   = Button(disp, text="OFF", width=3, height=3, command=captor_stat).grid(row=0,column=2)
	#captor_btn.pack()

		
Button(disp, text="submit", command=click).grid(row=3,column=0, sticky=W)

	# 4. another label
Label(disp, text="tampilkan output",bg="black", fg="White", font="none 12 bold").grid(row=4, column=0, sticky=W)
	# 5. text box
disp_out = Text(disp, width=30, height=20, wrap=WORD, background="white").grid(row=5, column=0, columnspan=2, sticky=W)
	# 6. dictionary
login_dict = {
	'name' : 'namamu',
	'pass' : 'passwordmu'	
	}
		

	#closing the window
Button(disp, text="CLOSE", width=3, height=3, command=close_window).grid(row=7,column=0)

	# run the mainloop
disp.mainloop() #mainloop

#-#if __name__ == '__main__':
#-#    main()

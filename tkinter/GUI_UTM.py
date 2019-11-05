######################## Underwater Trenching Mechine GUI #########################
# Author : Asri Gania
# Date   : August 1st 2019
###################################################################################

from tkinter import *

disp = Tk()

#---------------------------------------------------------------------------------

import tkinter
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

#========= Classes:

class Quaternion:
    """Quaternion Rotation:

    Class to aid in representing 3D rotations via quaternions.
    """
    @classmethod
    def from_v_theta(cls, v, theta):
        """
        Construct quaternions from unit vectors v and rotation angles theta

        Parameters
        ----------
        v : array_like
            array of vectors, last dimension 3. Vectors will be normalized.
        theta : array_like
            array of rotation angles in radians, shape = v.shape[:-1].

        Returns
        -------
        q : quaternion object
            quaternion representing the rotations
        """
        theta = np.asarray(theta)
        v = np.asarray(v)
        s = np.sin(0.5 * theta)
        c = np.cos(0.5 * theta)

        v = v * s / np.sqrt(np.sum(v * v, -1))
        x_shape = v.shape[:-1] + (4,)

        x = np.ones(x_shape).reshape(-1, 4)
        x[:, 0] = c.ravel()
        x[:, 1:] = v.reshape(-1, 3)
        x = x.reshape(x_shape)

        return cls(x)

    def __init__(self, x):
        self.x = np.asarray(x, dtype=float)

    def __repr__(self):
        return "Quaternion:\n" + self.x.__repr__()

    def __mul__(self, other):
        # multiplication of two quaternions.
        # we don't implement multiplication by a scalar
        sxr = self.x.reshape(self.x.shape[:-1] + (4, 1))
        oxr = other.x.reshape(other.x.shape[:-1] + (1, 4))

        prod = sxr * oxr
        return_shape = prod.shape[:-1]
        prod = prod.reshape((-1, 4, 4)).transpose((1, 2, 0))

        ret = np.array([(prod[0, 0] - prod[1, 1]
                         - prod[2, 2] - prod[3, 3]),
                        (prod[0, 1] + prod[1, 0]
                         + prod[2, 3] - prod[3, 2]),
                        (prod[0, 2] - prod[1, 3]
                         + prod[2, 0] + prod[3, 1]),
                        (prod[0, 3] + prod[1, 2]
                         - prod[2, 1] + prod[3, 0])],
                       dtype=np.float,
                       order='F').T
        return self.__class__(ret.reshape(return_shape))

    def as_v_theta(self):
        """Return the v, theta equivalent of the (normalized) quaternion"""
        x = self.x.reshape((-1, 4)).T

        # compute theta
        norm = np.sqrt((x ** 2).sum(0))
        theta = 2 * np.arccos(x[0] / norm)

        # compute the unit vector
        v = np.array(x[1:], order='F', copy=True)
        v /= np.sqrt(np.sum(v ** 2, 0))

        # reshape the results
        v = v.T.reshape(self.x.shape[:-1] + (3,))
        theta = theta.reshape(self.x.shape[:-1])

        return v, theta

    def as_rotation_matrix(self):
        """Return the rotation matrix of the (normalized) quaternion"""
        v, theta = self.as_v_theta()

        shape = theta.shape
        theta = theta.reshape(-1)
        v = v.reshape(-1, 3).T
        c = np.cos(theta)
        s = np.sin(theta)

        mat = np.array([[v[0] * v[0] * (1. - c) + c,
                         v[0] * v[1] * (1. - c) - v[2] * s,
                         v[0] * v[2] * (1. - c) + v[1] * s],
                        [v[1] * v[0] * (1. - c) + v[2] * s,
                         v[1] * v[1] * (1. - c) + c,
                         v[1] * v[2] * (1. - c) - v[0] * s],
                        [v[2] * v[0] * (1. - c) - v[1] * s,
                         v[2] * v[1] * (1. - c) + v[0] * s,
                         v[2] * v[2] * (1. - c) + c]],
                       order='F')
        return mat.T.reshape(shape + (3, 3))
        

class CubeAxes(Axes):
    """Axes to show 3D cube

    The cube orientation is represented by a quaternion.
    The cube has side-length 2, and the observer is a distance zloc away
    along the z-axis.
    """
    face = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1], [1, 1]])
    faces = np.array([np.hstack([face[:, :i],
                                 np.ones((5, 1)),
                                 face[:, i:]]) for i in range(3)] +
                     [np.hstack([face[:, :i],
                                 -np.ones((5, 1)),
                                 face[:, i:]]) for i in range(3)])
    stickercolors = ["#ffffff", "#00008f", "#ff6f00",
                     "#ffcf00", "#009f0f", "#cf0000"]

    def __init__(self, *args, **kwargs):
        self.start_rot = Quaternion.from_v_theta((1, -1, 0), -np.pi / 6)
        self.current_rot = self.start_rot

        self.start_zloc = 10.
        self.current_zloc = 10.

        # Define movement for up/down arrows or up/down mouse movement
        self._ax_UD = (1, 0, 0)
        self._step_UD = 0.01

        # Define movement for left/right arrows or left/right mouse movement
        self._ax_LR = (0, -1, 0)
        self._step_LR = 0.01

        # Internal variables.  These store states and data
        self._active = False
        self._xy = None
        self._cube_poly = None

        # initialize the axes.  We'll set some keywords by default
        kwargs.update(dict(aspect='equal', xlim=(-1.5, 1.5), ylim=(-1.5, 1.5),
                           frameon=False, xticks=[], yticks=[]))
        super(CubeAxes, self).__init__(*args, **kwargs)

        # connect some GUI events
        self.figure.canvas.mpl_connect('button_press_event',
                                       self._mouse_press)
        self.figure.canvas.mpl_connect('button_release_event',
                                       self._mouse_release)
        self.figure.canvas.mpl_connect('motion_notify_event',
                                       self._mouse_motion)
        self.figure.canvas.mpl_connect('key_press_event',
                                       self._key_press)
        self.figure.canvas.mpl_connect('key_release_event',
                                       self._key_release)

        self.draw_cube()

        self.figure.text(0.05, 0.05, ("Drag Mouse or use arrow keys to change "
                                      "perspective.\n"
                                      "hold shift to rotate around z-axis"),
                         ha='left', va='bottom')

    @staticmethod
    def project_points(pts, rot, zloc):
        """Project points to 2D given a rotation and a view

        pts is an ndarray, last dimension 3
        rot is a Quaternion object, containing a single quaternion
        zloc is a distance along the z-axis from which the cube is being viewed
        """
        R = rot.as_rotation_matrix()
        Rpts = np.dot(pts, R.T)

        xdir = np.array([1., 0, 0])
        ydir = np.array([0, 1., 0])
        zdir = np.array([0, 0, 1.])

        view = zloc * zdir
        v2 = zloc ** 2

        result = []
        for p in Rpts.reshape((-1, 3)):
            dpoint = p - view
            dproj = 0.5 * dpoint * v2 / np.dot(dpoint, -1. * view)
            result += [np.array([np.dot(xdir, dproj),
                                 np.dot(ydir, dproj),
                                 np.dot(zdir, dpoint / np.sqrt(v2))])]
        return np.asarray(result).reshape(pts.shape)

    def draw_cube(self, rot=None, zloc=None):
        """Draw a cube on the axes.

        The first time this is called, it will create a set of polygons
        representing the cube faces.  On initial calls, it will update
        these polygon faces with a given rotation and observer location.

        Parameters
        ----------
        rot : Quaternion object
            The quaternion representing the rotation
        zloc : float
            The location of the observer on the z-axis (adjusts perspective)
        """
        if rot is None:
            rot = self.current_rot
        if zloc is None:
            zloc = self.current_zloc

        self.current_rot = rot
        self.current_zloc = zloc

        if self._cube_poly is None:
            self._cube_poly = [plt.Polygon(self.faces[i, :, :2],
                                           facecolor=self.stickercolors[i],
                                           alpha=0.9)
                               for i in range(6)]
            [self.add_patch(self._cube_poly[i]) for i in range(6)]

        faces = self.project_points(self.faces, rot, zloc)
        zorder = np.argsort(np.argsort(faces[:, :4, 2].sum(1)))

        [self._cube_poly[i].set_zorder(10 * zorder[i]) for i in range(6)]
        [self._cube_poly[i].set_xy(faces[i, :, :2]) for i in range(6)]

        self.figure.canvas.draw()

    def _key_press(self, event):
        """Handler for key press events"""
        if event.key == 'shift':
            self._ax_LR = (0, 0, 1)
            self._shift_on = True

        elif event.key == 'right':
            self.current_rot = (self.current_rot
                                    * Quaternion.from_v_theta(self._ax_LR,
                                                              self._step_LR))
        elif event.key == 'left':
            self.current_rot = (self.current_rot
                                * Quaternion.from_v_theta(self._ax_LR,
                                                          -self._step_LR))
        elif event.key == 'up':
            self.current_rot = (self.current_rot
                                * Quaternion.from_v_theta(self._ax_UD,
                                                          self._step_UD))
        elif event.key == 'down':
            self.current_rot = (self.current_rot
                                * Quaternion.from_v_theta(self._ax_UD,
                                                          -self._step_UD))
        self.draw_cube()

    def _key_release(self, event):
        """Handler for key release event"""
        if event.key == 'shift':
            self._ax_LR = (0, -1, 0)

    def _mouse_press(self, event):
        """Handler for mouse button press"""
        if event.button == 1:
            self._active = True
            self._xy = (event.x, event.y)

    def _mouse_release(self, event):
        """Handler for mouse button release"""
        if event.button == 1:
            self._active = False
            self._xy = None

    def _mouse_motion(self, event):
        """Handler for mouse motion"""
        if self._active:
            dx = event.x - self._xy[0]
            dy = event.y - self._xy[1]
            self._xy = (event.x, event.y)
            rot1 = Quaternion.from_v_theta(self._ax_UD,
                                           self._step_UD * dy)
            rot2 = Quaternion.from_v_theta(self._ax_LR,
                                           self._step_LR * dx)

            self.current_rot = (self.current_rot * rot1 * rot2)
            self.draw_cube()

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

	disp.title("Underwater Trenching Mechine GUI")
	disp.minsize(width=1020, height=600)
	disp.maxsize(width=1080, height=720)
	#disp.configure(background="blue")

	# label
	Label (disp, text="UNDERWATER TRENCHING MECHINE INTERFACE", bg="black", fg="White", font="none 12 bold").pack(anchor=CENTER)
	#Label (disp, text="CONTROL AND MONITORING", bg="black", fg="White", font="none 12 bold").pack(anchor=CENTER)

	
	
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

import pycompadre
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

''' Interactive example of weighting kernels in pycompadre

The weighting kernels used in the GMLS class in the function Wab allow users
to vary two parameters. This tool gives users the ability to vary these two
parameters and weighting type and see the effect visually.
'''

# initialize Kokkos
kp = pycompadre.KokkosParser()

# initialize parameters
wt = pycompadre.WeightingFunctionType.Power
x = np.linspace(-2.0, 2.0, 1000)
h = 1.0
p = 2
n = 1

def approximate(wt, h, p, n):
    y = np.array([pycompadre.Wab(xin,h,wt,p,n) for xin in x], dtype='f8')
    return y

# get initial data
y = approximate(wt, h, p, n)

# plot initial data
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
d, = plt.plot(x, y, c='#0000FF', linewidth=4, zorder=1)
ax.set(xlabel='r', ylabel='',
       title='Kernel Evaluation')
ax.grid()
ax.margins(x=0)
axcolor = 'lightgoldenrodyellow'
ax.autoscale(True)
ax.relim()
ax.autoscale_view()
ax.autoscale(False)

# axes for sliders and radio buttons
ax_p = plt.axes([0.25, 0.125, 0.65, 0.03], facecolor='white')
ax_n = plt.axes([0.25, 0.075, 0.65, 0.03], facecolor='white')
ax_weighting_type = plt.axes([0.015, 0.25, 0.15, 0.35], facecolor=axcolor)

# sliders
delta_f = 4.0/200
sl_p = Slider(ax_p, 'P', valmin=0.0, valmax=6.0, valinit=2, valstep=1, color=None, initcolor='black')
sl_n = Slider(ax_n, 'N', valmin=0.0, valmax=6.0, valinit=1, valstep=1, color=None, initcolor='black')

#radios
rad_weighting_type = RadioButtons(ax_weighting_type, ('Power', 'Cubic Spl.', 'Cosine', 'Gaussian', 'Sigmoid'), active=0)

def update(val):
    global wt
    y = approximate(wt, h, int(sl_p.val), int(sl_n.val))
    d.set_ydata(y)
    fig.canvas.draw_idle()

# register objects using update
sl_p.on_changed(update)
sl_n.on_changed(update)

def weighting_type_update(label):
    weighting_type_dict = {'Power': pycompadre.WeightingFunctionType.Power, 'Cubic Spl.': pycompadre.WeightingFunctionType.CubicSpline, 'Cosine': pycompadre.WeightingFunctionType.Cosine, 'Gaussian': pycompadre.WeightingFunctionType.Gaussian, 'Sigmoid': pycompadre.WeightingFunctionType.Sigmoid}
    global wt
    wt = weighting_type_dict[label]
    if (label=='Power'):
        ax_p.set_visible(True)
        ax_n.set_visible(True)
    elif (label=='Cubic Spl.'):
        ax_p.set_visible(False)
        ax_n.set_visible(False)
    elif (label=='Cosine'):
        ax_p.set_visible(False)
        ax_n.set_visible(False)
    elif (label=='Gaussian'):
        ax_p.set_visible(True)
        ax_n.set_visible(False)
    elif (label=='Sigmoid'):
        ax_p.set_visible(True)
        ax_n.set_visible(True)

    y0 = approximate(wt, h, 0, 0)
    y1 = approximate(wt, h, 0, 6)
    y2 = approximate(wt, h, 6, 0)
    y3 = approximate(wt, h, 6, 6)

    dy0, = ax.plot(x, y0, c='#0000FF', linewidth=4, zorder=1)
    dy1, = ax.plot(x, y1, c='#0000FF', linewidth=4, zorder=1)
    dy2, = ax.plot(x, y2, c='#0000FF', linewidth=4, zorder=1)
    dy3, = ax.plot(x, y3, c='#0000FF', linewidth=4, zorder=1)
    ax.autoscale(True)
    d.set_ydata(y0)
    ax.relim()
    ax.autoscale_view()
    ax.autoscale(False)

    dy0.remove()
    dy1.remove()
    dy2.remove()
    dy3.remove()

    update(0)

# register objects using weighting_type_update
rad_weighting_type.on_clicked(weighting_type_update)

plt.show()
del kp

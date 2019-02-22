
#Meant to monte-carlo integrate a gaussian
from numpy import sqrt
import numpy as np
from matplotlib import pyplot as plt
from random import uniform

#tweakables
leftlim = -1
rightlim = 1
sample_number = 10000
box_area = 4 # area of a rectangle around the gaussian with unit height
probability = np.pi/box_area


#Defining the gaussian
func = lambda x: sqrt(1-x**2)
x = np.linspace(leftlim, rightlim, 100000)
func2 = lambda x: -1*sqrt(1-x**2)

topy = func(x)
bottomy = func2(x)


counter = 0
below = 0
above = 0
plt.subplot(2, 1, 1)
plt.scatter(x, topy, color = 'black')	
plt.xlim(leftlim*2, rightlim*2)
plt.ylim(-1, 1)
plt.scatter(x, bottomy, color = 'black')
#plt.ion()
#plt.show()
while counter < sample_number:
	new_x = uniform(leftlim, rightlim)
	new_y = uniform(-1, 1)
	y_here = func(new_x)
	if sqrt(new_x**2 + new_y**2) <= 1:
		below += 1
		this_color = 'blue'	
	else:
		above += 1
		this_color = 'red'
#	plt.scatter(new_x, new_y, color = this_color, s = 5)
	counter += 1
	ratio = float(below)/(above+below)
	new_pi = ratio*box_area
#	print 'probability, ratio, new_pi: ', probability, ratio, new_pi
	plt.subplot(2, 1, 1)
	plt.scatter(new_x, new_y, color = this_color, marker = '.', s= 5)
	ratio_now =new_pi/np.pi
	plt.title('$y = exp(-x^2)$. Calculated $\pi$ = {0:.6f}, ratio to real $\pi$ = {1:.6f}'.format(new_pi, ratio_now))
	plt.subplot(2, 1, 2)
	plt.scatter(counter, new_pi, color = 'blue', s = 5)
	plt.scatter(counter, ratio_now, color = 'red', s = 5)
	plt.ylim([np.pi-4, np.pi+2])
	plt.hlines(np.pi, 0, sample_number)
	plt.hlines(1, 0, sample_number)
	plt.xlim([0, counter])
	plt.title('Blue: calculated $\pi$. Red: Ratio to real $\pi$.')
	plt.xlabel('Frame count')
	plt.savefig('monte_frames/frame_{0}'.format(counter))
#	plt.pause(0.0000001)

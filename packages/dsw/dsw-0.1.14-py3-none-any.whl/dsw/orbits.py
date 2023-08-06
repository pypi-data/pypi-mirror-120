import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from rebound.plotting import fading_line
import numpy as np

def orbit_plot(objects, iter, tail_length):

  if iter < tail_length:
    tail_start = 0
  else: 
    tail_start = iter - tail_length + 1
  
  tail_end = iter + 1

  clear_output(wait=True)

  line_width = 2

  line_collections = []
  circles = []

  for object in objects:

    #line_collections.append(fading_line(np.transpose(object)[0], np.transpose(object)[1], color='white', lw=line_width))
    #circles.append(plt.Circle((object[-1][0], object[-1][1]) , 0.05, color='r', zorder = 10))

    line_collections.append(fading_line(np.transpose(object[tail_start:tail_end])[0], np.transpose(object[tail_start:tail_end])[1], color='white', lw=line_width))
    circles.append(plt.Circle((object[tail_start:tail_end][-1][0], object[tail_start:tail_end][-1][1]) , 0.05, color='r', zorder = 10))

  lim = 2.0
  fontsize = 9
  padding = 9

  plt.style.use('dark_background')

  params = {'grid.alpha': 0.6,
            'grid.color': '#cccccc'}
  plt.rcParams.update(params)


  fig = plt.figure(figsize=(10, 10), dpi=150, facecolor='black', edgecolor='black')

  ax = plt.axes()

  ax.set_xlim([-lim, lim])
  ax.set_ylim([-lim, lim])
  ax.set_aspect('equal')

  ax.set_xlabel('[AU]', fontsize = fontsize)
  ax.set_ylabel('[AU]', fontsize = fontsize)
  ax.set_title('ORBIT PLOT', fontsize = fontsize, pad = padding)

  for i in range(len(objects)):

    ax.add_collection(line_collections[i])
    ax.add_patch(circles[i])

  plt.xticks(fontsize = fontsize - 2)
  plt.yticks(fontsize = fontsize - 2)

  plt.tight_layout(pad=20.0)
  plt.grid(True)
  plt.show()

def position(particle):

  return [particle.x, particle.y, particle.z]

def velocity(particle):

  return [particle.vx, particle.vy, particle.vz]  

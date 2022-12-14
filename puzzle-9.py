import numpy as np
from matplotlib import pyplot as plt
from celluloid import Camera
from tqdm import tqdm

# import data

INPUTFILE = 'input-9-test2.txt'

import numpy as np

with open(INPUTFILE, 'r') as file:
    input = file.read()
rows = input.split("\n")

# helper functions

def update_head(head, direction:str):
  if direction == "R":
    head[0] += 1
  elif direction == "L":
    head[0] -= 1
  elif direction == "U":
    head[1] += 1
  elif direction == "D":
    head[1] -= 1
  return head

def update_tail(head, tail):
  for xy in range(2):
    if abs(head[xy]-tail[xy]) > 1:
      tail[xy] = tail[xy] + np.sign(head[xy] - tail[xy])
      tail[(xy+1)%2] = head[(xy+1)%2]
  return tail

# create animation

fig = plt.figure()
#camera = Camera(fig)

# iteration

snake = np.array([[0,0] for _ in range(10)])

visited = np.array([0,0])

for row in tqdm(rows):
  # calculate next iteration
  command = row.split(" ")
  for _ in range(int(command[1])):
    snake[0] = update_head(snake[0], command[0])
    for i in range(1,len(snake)):
      snake[i] = update_tail(snake[i-1], snake[i])
    if tuple(snake[-1]) not in visited:
      np.append(visited,(tuple(snake[-1])))
  
    # plot image
    #plotsnake = np.array(snake)
    #plotvisited = np.array(visited_positions)

    plt.scatter(snake[:,0], snake[:,1], c='k')
    plt.scatter(visited[:,0], visited[:,1],
      c=range(len(visited)), cmap="autumn_r")
    #plt.axis([-15,15,-10,20])
    plt.pause(0.2)
    #camera.snap()

# save animation

plt.show()
#animation = camera.animate(interval=200)
#animation.save('output.gif')
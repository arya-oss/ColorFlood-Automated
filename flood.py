#!/usr/bin/env python

import cv2
import numpy as np
import copy
import sets
from os import system

system("adb shell screencap -p /sdcard/flood.png")
system("adb pull /sdcard/flood.png")
system("adb shell rm /sdcard/flood.png")

im = cv2.imread('flood.png', cv2.IMREAD_GRAYSCALE)
im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
im = im[74:422, 7:355]
colors = {91:0, 147:1, 143:2, 136:3, 187:4, 234:5}
grid = [[0 for i in range(0, 12)] for j in range(0,12)]

for i in range(0, 12):
    for j in range(0, 12):
        grid[i][j] = colors[im[29*i+14][29*j+14]]

class Game:
	def __init__(self, grid, width, height, num_colors):
		self._grid = grid
		self._width = width
		self._height = height
		self._num_colors = num_colors

	def neighbour(self, x, y):
	    retval = sets.Set([])

	    col = self._grid[x][y]
	    stk = []
	    stk.append((x,y))
	    
	    while len(stk) > 0:
	        curr = stk.pop()
	        retval.add(curr)
	        c_x = curr[0]
	        c_y = curr[1]

	        nbs = [(c_x,c_y+1),(c_x,c_y-1),(c_x+1,c_y),(c_x-1,c_y)]
	        for n in nbs:
	            if n[0] < self._width and n[0] >=0 and n[1] < self._height and n[1] >= 0:
	                if self._grid[n[0]][n[1]] == col and not (n in retval):
	                    stk.append(n)   
	    # return
	    return retval
	
	def flood(self, x, y, c):
		pts = self.neighbour(x,y)
		for p in pts:
			self._grid[p[0]][p[1]] = c
	def greedy(self):
		retval = []
		g = copy.deepcopy(self)
		c = g.neighbour(0,0)
		S = g._width * g._height
		# continue until all cells have the same color
		while len(c) != S:
		# attempt all flood options
			cps = []
			for i in xrange(0, self._num_colors+1):
				cps.append(copy.deepcopy(g))
			csz = [0 for i in xrange(0, self._num_colors+1)]
			for i in xrange(0,self._num_colors+1):
				cps[i].flood(0,0,i)
				csz[i] = len(cps[i].neighbour(0,0))

			# best move
			max_index = csz.index(np.max(csz))
			g = cps[max_index]
			c = g.neighbour(0,0)
			# append to array
			retval.append(max_index)
		# return
		return retval
	def print_grid(self):
		for b in self._grid:
			print b

g = Game(grid, 12, 12, 6)
moves = g.greedy()
# g.print_grid()
tap_pos = { 0: (60, 1000), 1:(180, 1000), 2:(300, 1000), 3:(420, 1000), 4:(540, 1000), 5:(660, 1000)}
print len(moves)
if len(moves) <=22:
	for i in moves:
		cmd = "adb shell input tap {0} {1}".format(tap_pos[i][0], tap_pos[i][1])
		system(cmd)
# cv2.imshow('Color Flood', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

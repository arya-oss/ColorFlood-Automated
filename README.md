## Color Flood

### Game Description

The objective of this game is to flood fill the entire board with one color. This objective has to be
completed within 22 steps for 12x12 board.
**Playstore Link:** [Color Flood](https://play.google.com/store/apps/details?id=com.wetpalm.colorflood&hl=en)

![Color Flood](/Images/play_flood.png)

**Difficulty Level:** Moderate

### Overview

The cell are detected using image processing. The solution of game is calculated using Naive greedy approach. The screen is touched by using the adb tool library.

### Requirements

- An Android Device with the this game installed in it.
- OpenCV-Python: Used for Image Processing.
- Python 2.8: for algorithma and Images processing. 

### Block Diagram

![BlockDiagram](/Images/BlockDiagram.png)

### Tutorial

#### Step 1: Detecting the colored cells

This is done by using OpenCV. The image that is captured from android device using ADB tool and from colored cell matrix formed. This grid is goes input to solving algorithm.

- For capturing an image from adb tool.
```python
	system('adb shell screencap -p /sdcard/flood.png')
	system('adb pull /sdcard/flood.png')

``` 
- Extracting colors from grid

```python
	im = cv2.imread('flood.png', cv2.IMREAD_GRAYSCALE)
	# resize the image
	im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
	
	# Crop the image part contains all colored cell
	im = im[74:422, 7:355]
	
	# Mapping diffenrent color (grayscale) to a given value
	colors = {91:0, 147:1, 143:2, 136:3, 187:4, 234:5}
	
	grid = [[0 for i in range(0, 12)] for j in range(0,12)]
	for i in range(0, 12):
    	for j in range(0, 12):
        	grid[i][j] = colors[im[29*i+14][29*j+14]] # centre pixel a cell
```


#### Step 2: Algorithm

The algorithm is based on graph breadth first traversal with greedy approach which is from top-left corner which color covers
maximum cells.

- counting neighbours of a cell (which is connected in any one of direction (UP, DOWN, LEFT, RIGHT)
```python
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
```

- Take the best color from current states

```python
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
```
- This algorithm not ensures that each time we get optimal solution i.e, 22 moves .

#### Step 3: Simulating Touch

Touch is simlated using adb tool. Tap position of all six colored cell at bottom determined from captured image
and stored. Algorithm return result set which containes color codes.

if result set is optimal then touch is simulated.

```python
	# determined from captured image
	tap_pos = { 0: (60, 1000), 1:(180, 1000), 2:(300, 1000), 3:(420, 1000), 4:(540, 1000), 5:(660, 1000)}
	for i in moves:
		cmd = "adb shell input tap {0} {1}".format(tap_pos[i][0], tap_pos[i][1])
		system(cmd)
```

### Conclusions

Whole Image processing tested on Moto G3 device, it will work for any device of resolution 1280x720.
 
The algorithm based on greedy approach which is not suitable for this game so it won't work many times.


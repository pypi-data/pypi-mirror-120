#! /usr/bin/env python3


def getnet(fn):
	""" This module will read a net file "fn" containing
	components and node connection specifications. It will
	output the matrix node equations. Format of the 'net'
	data file example of one line:
		c1+y1+A*ya,3,4   equation, node 3, mutual (adjacent node 4
		A zero in the third column refers to common or ground.
	Input: fn = filename of net file (connection list)
	Output: square matrix (list of lists) of size equalto the number of
	voltage nodes."""

	with open(fn, 'r') as equfile:
		nbnodes = 0
		ll = []
		for line in equfile:
			if line[0] == '#' or len(line) < 5: continue
			e,n,m = line.split(',')
			sm = m[:m.find('#')]  # strip off comment
			sm = sm.strip()
			ll.append((e,n,sm))
			if int(n) > nbnodes: nbnodes = int(n)

		# Start building matrix
		mat = [['0' for i in range(nbnodes)] for j in range(nbnodes)]
		for tup in ll:
			e,n,mn = tup
			row = int(n)-1
			if mn == '0':
				col = row
			else:
				col = int(mn)-1
			mat[row][col] = e
		return mat

if __name__ == "__main__":

	mat = getnet("examples/BainterFilter.net")
	for i in range(len(mat)):
		print(mat[i])
	




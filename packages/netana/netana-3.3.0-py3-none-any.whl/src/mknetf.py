#! /usr/bin/env python3

import os, time

def mknetf(fn,mat):

	""" This module will write a net file "fn" containing
	equiations and node connection specifications.
	Output: the matrix equations and component connections. 
	Format of the 'net data file example of one line:
		c1+y1+A*ya,3,4   equation, node 3, mutual node 4
		A zero in the third column refers to common or ground.
	Input: fillename(fn) and square matrix of equation strings and
		zero strings('0') repreesenting NO equation. 
	Output: File(fn) of node/mask equations and connections."""


	sz = len(mat)
	with open(fn, 'w') as outf:
		# Write header to output file.
		pn = os.path.basename(fn[:-4])
		date = time.ctime()
		outf.write("# Net file for project: {:s} \n".format(pn))
		outf.write("# Produced by Natana.\n")
		outf.write("# Date: {:s}\n\n".format(date))

		for r in range(sz):
			for c in range(sz):
				mnode = '0'
				if mat[r][c] == '0': continue  # no node equ
				else:
					equstr = mat[r][c] # get node equation
					if r==c : node = str(r+1)   # on diggonal get node n
					else: mnode = str(c+1) # get mutial node number
					outf.write( equstr+','+node+','+mnode+'\n')
                

if __name__ == "__main__":

    mat = [['y1','0','0','0','d2'],
           ['m1','y2','0','0','0'],
           ['0','m2','y3','0','0'],
           ['0','0','m3','y4','0'],
           ['d1','0','0','m4','y5']]

    fn = "./test.net"
    mknetf(fn,mat)

    

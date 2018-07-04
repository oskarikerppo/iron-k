import numpy as np
def main():
	x = np.array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
	 [ 0.,  0.,  0., -6.,  0.,  0.,  0.,  0.],
	 [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
	 [ 0.,  0.,  0.,  3.,  0.,  0.,  0.,  0.],
	 [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
	 [ 6., 0.,  0.,  0.,  0.,  0.,  0.,  0.],
	 [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
	 [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])


	unique, counts = np.unique(x,return_counts=True)

	piece_counts = dict(zip(unique,counts))
	piece_counts_keys = piece_counts.keys()
	print piece_counts
	print piece_counts_keys


	if 1 not in piece_counts_keys and -1 not in piece_counts_keys:
		print "level 1"
		if 5 not in piece_counts_keys and -5 not in piece_counts_keys:
			print "level 2"
			if 4 not in piece_counts_keys and -4 not in piece_counts_keys:
				print "level 3"
				if 3 not in piece_counts_keys and -3 not in piece_counts_keys:
					print "level 4"
					return "Insufficient material"
				elif (piece_counts.get(3,0) < 2 and piece_counts.get(2,0) == 0 or piece_counts.get(3,0) == 0) and (piece_counts.get(-3,0) < 2 and piece_counts.get(-2,0) == 0 or piece_counts.get(-3,0) == 0):
					print "level 4 else"
					return "Insufficient material"

kulli = main()
print kulli
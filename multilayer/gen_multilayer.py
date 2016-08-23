import numpy as np
import random
import scipy
import scipy.stats as stats
import matplotlib.pyplot as plt
import sys

def draw_powerlaw_distribution(a, n):
	size = n
	pld = np.random.power(a, size)
	print pld
	#powerpdf = stats.powerlaw.pdf(xx, 5)
	#print powerpdf

	'''plt.figure()
	plt.hist(pld, bins=50, normed=False)
	plt.plot(xx, powerpdf,'r-')
	plt.show()'''

'''def truncated_power_law(a, m):
    x = np.arange(1, m+1, dtype='float')
    pmf = 1/x**a
    pmf /= pmf.sum()
    return stats.rv_discrete(values=(range(1, m+1), pmf))

def draw_pw_distribution(a, m):
	d = truncated_power_law(a=a, m=m)

	N = m**4
	sample = d.rvs(size=N)

	plt.hist(sample, bins=np.arange(m)+0.5)
	plt.show()'''

def main(argv):
	exponent = 2.5
	# number of edges
	m = 0
	# number of nodes
	n = 1000

	draw_powerlaw_distribution(exponent, n)

if __name__  == "__main__":
	main(sys.argv[1:])
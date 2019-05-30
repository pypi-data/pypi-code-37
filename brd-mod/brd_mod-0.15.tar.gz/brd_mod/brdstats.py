import numpy as np 
import statsmodels.api as sm 
import math
import matplotlib.pyplot as plt 
from scipy.integrate import quad
import sys
import os
import logging
from brd_mod.brdgeo import *
from brd_mod.brdecon import *


def dot(x, y):
	'''
	Dot product between two vector-like arrays
	'''
	if len(x) != len(y):
		print("Array sizes are not equal.")
		return

	sum = 0
	for i in range(0, len(x)):
		sum += (x[i]*y[i])

	return sum

def sum(x):
	'''
	Calculates sum of array
	'''
	total= 0
	for i in range(0, len(x)):
		total += x[i]

	return total

def mean(x):
	'''
	Calculates the mean value of an array
	'''
	return sum(x)/len(x)

def square(x):
	'''
	Squares each value of an array
	'''
	series= []
	for i in range(0, len(x)):
		series.append(x[i]**2)

	return series

def variance(x):
	'''
	Calculates population variance of an array
	'''
	sample= mean(x)
	ses= []
	for i in range(0, len(x)):
		ses.append((x[i]-sample)**2)

	return sum(ses)/(len(x))

def covariance(x, y):
	'''
	Calculates co-variance between two arrays
	'''
	if len(x) != len(y):
		print("Array sizes are not equal.")
		return

	x_mean= mean(x)
	y_mean= mean(y)
	x_ses= []
	y_ses= []
	for i in range(0, len(x)):
		x_ses.append(x[i]-x_mean)
		y_ses.append(y[i]-y_mean)

	return dot(x_ses, y_ses)/len(x)

def std_dev(x):
	'''
	Calculates population standard deviation
	of an array
	'''
	return math.sqrt(variance(x))

def median(x):
	'''
	Calculates the median value of an array
	'''
	x.sort()
	n= len(x)
	if n < 1:
		print("List too short.")
		return

	if n % 2 ==1:
		return x[n//2]

	else:
		return sum(x[n//2-1:n//2+1])/2.0

def corr_coef(x, y):
	'''
	Calculates Pearson Correlation Coefficient
	of an array
	'''
	if len(x) != len(y):
		print("Array sizes are not equal.")
		return
	
	x_mean= mean(x)
	y_mean= mean(y)
	length= len(x)
	xx_arr= []
	yy_arr= []
	for i in range(0, len(x)):
		xx_arr.append((x[i]**2)-length*(x_mean**2))
		yy_arr.append((y[i]**2)-length*(y_mean**2))
		
	ss_xy = ((dot(x, y))-(length*x_mean*y_mean))
	ss_xx= sum(xx_arr)
	ss_yy= sum(yy_arr)

	return (length*dot(x, y) - sum(x)*sum(y))/math.sqrt(( \
		length*sum(square(x))-sum(x)**2)*(length*sum(square(y))-sum(y)**2))

def cointegration_strength(data1, data2):
	'''
	Runs Cointegration Test on Two Datasets
	data1= data series 1
	data2= data series 2
	Returns t-stat and p-value of Cointegration
	'''
	data1= series_to_array(data1).flatten()
	data2= series_to_array(data2).flatten()

	if len(data1) != len(data2):
		return "Sizes do not Match"

	return ts.coint(data1, data2)[:2]

def norm_pdf(x, mean=0, std=1):
	'''
	Probability density function using
	normal distribution with pre-specified
	mean and standard deviation (default: standard
	normal distribution)
	'''
	expo= -(x-mean)**2/(2*std**2)
	prefix= 1/math.sqrt(2*math.pi*std**2)
	return prefix*math.exp(expo)

def error_func(t):
	'''
	Integrand for cumulative distribution function
	for normal distribution
	'''
	return math.exp(-t**2)

def norm_cdf(x, mean=0, std=1):
	'''
	Cumulative distribution function using
	normal distribution with pre-specified
	mean and standard deviation (default: standard
	normal distribution)
	'''
	inp= (x-mean)/(std*math.sqrt(2))
	integ =quad(error_func, 0, inp)[0]
	return (1/2)*(1+(2/math.sqrt(math.pi))*integ)

def skewness(x):
	'''
	Calculates skewness of an array from a 
	standard normal distribution
	'''
	x_mean= mean(x)
	length= len(x)
	x_cu= []
	for i in range(0, len(x)):
		x_cu.append(math.pow(x[i]-x_mean, 3))

	return sum(x_cu)/(math.pow(std_dev(x),3))

def kurtosis(x):
	'''
	Calculates kurtosis of an array from a
	standard normal distribution
	'''
	x_mean= mean(x)
	length= len(x)
	x_qu= []
	for i in range(0, len(x)):
		x_qu.append(math.pow(x[i]-x_mean, 4))

	return sum(x_qu)/(length*math.pow(std_dev(x), 4))

def step_generation(x_min=-3, x_max=3, step=0.0001):
	'''
	Generates an array of higher resolution
	between two boundaries and a specified 
	step value
	'''
	n = int(round((x_max - x_min)/float(step)))
	return([x_min + step*i for i in range(n+1)])

def plot_norm(mean=0, std=1, pdf=True, x_min=-3, x_max=3, step=0.0001):
	'''
	Plots a normal distribution from a 
	pre-specified mean and standard deviation
	using two boundaries and a specified step
	value
	'''
	x_list= step_generation(x_min, x_max, step)
	y_list= []
	for x in x_list:
		if pdf:
			y_list.append(norm_pdf(x, mean, std))
		else:
			y_list.append(norm_cdf(x, mean, std))

	plt.plot(x_list, y_list)
	plt.show()

def boxcox_transformation(data, param):
	'''
	BoxCox Transformation on Dataset:
	log(y_t) if param=0
	(y_t^param-1)/param otherwise
	'''
	return data.apply(boxcox_aux, args=(param,))

def boxcox_aux(param, value):
	'''
	Auxillary Function to Apply BoxCox to Individual Data
	'''
	if param ==0:
		return math.log(value)
	else:
		return (math.pow(value, param)-1)/float(param)
 
def reverse_boxcox_transformation(data, param):
	'''
	BoxCox Transformation on Dataset:
	log(y_t) if param=0
	(y_t^param-1)/param otherwise
	'''
	return data.apply(reverse_boxcox_aux, args=(param,))

def reverse_boxcox_aux(param, value):
	'''
	Auxillary Function to Apply Reverse BoxCox to Individual Data
	'''
	if param ==0:
		return math.exp(value)
	else:
		try:
			base= (param*value)+1
			expo= 1/param
			return math.pow(base, expo)
		except:
 			print("Negative Value Encountered, Reverse Transformation Failed.")
 			return -1

def back_transform(data, param):
	'''
	Back-Transforms Mean for Box-Cox Transformation
	'''	
	var= data.var()
	return data.apply(back_transform_aux, args=(param, var,))

def back_transform_aux(param, var, value):
	'''
	Auxillary Function to Back-Transform Mean for Individual Data
	'''
	if param==0:
		return math.exp(value)*(1+(var/2))
	else:
		try:
			base= (param*value+1)
			expo= 1/param
			expart= math.pow(base, expo)
			varnum= var*(1-param)
			varden= 2*math.pow(base, 2)
			return expart*(1+(varnum/varden))
		except:
			print("Negative Value Encountered, Reverse Transformation Failed.")
			return -1

def log_transformation(data):
	'''
	Basic function to take log of each data point
	'''
	return data.apply(math.log)

def set_union(x, y):
	'''
	Returns array that represents the sorted union
	of two input arrays
	'''
	temp= x
	for i in y:
		try:
			val= temp.index(i)

		except:
			temp.append(i)

	temp.sort()
	return temp

def set_intersection(x, y):
	'''
	Returns array that represents the sorted intersection
	of two input arrays
	'''
	temp= []
	for i in x:
		try:
			val= y.index(i)
			if val > -1:
				temp.append(i)
		except:
			pass

	temp.sort()
	return temp
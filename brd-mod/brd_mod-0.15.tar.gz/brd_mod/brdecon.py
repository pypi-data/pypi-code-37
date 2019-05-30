import pandas as pd 
import numpy as np 
import numpy.random as npr
import statsmodels as sm 
import statsmodels.tsa.stattools as ts
import math
import scipy
import matplotlib.pyplot as plt
from scipy import log,exp,sqrt,stats
import sys
import os
import logging
from brd_mod.brdstats import *
from brd_mod.brdgeo import *


def discrete_future_value(x,r,n):
	'''
	Discrete Future Value of Money over Time
	x= initial capital
	r= rate (0.n format)
	n= time increment
	'''
	return x*(1+r)**n

def discrete_present_value(x,r,n):
	'''
	Discrete Present Value of Money from Time
	x= future capital
	r= rate (0.n format)
	n= time increment
	'''
	return x*(1+r)**-n
	
def continuous_future_value(x,r,t):
	'''
	Continuous Future Value of Money over Time
	x= initial capital
	r= rate (0.n format)
	n= time increment
	'''
	return x*math.exp(r*t)
	
def continuous_present_value(x,r,t):
	'''
	Continuous Present Value of Money from Time
	x= future capital
	r= rate (0.n format)
	n= time increment
	'''
	return x*math.exp(-r*t)

def value_at_risk(position, c, mu, sigma):
	'''
	Calculate Basic Value at Risk (VAR)
	position= total value of investment
	c= confidence level
	mu= mean return
	sigma= sd of return
	'''
	alpha=stats.norm.ppf(1-c)
	var = position*(mu-sigma*alpha)
	return var
	
def value_at_risk_long(S, c, mu, sigma, n):
	'''
	Calculate Basic Value at Risk (VAR) into the Future
	S= total value of investment
	c= confidence level
	mu= mean return
	sigma= sd of return
	n= time increment
	'''
	alpha=stats.norm.ppf(1-c)
	var = S*(mu*n-sigma*alpha*np.sqrt(n))
	return var

def imperial_returns(data):
	'''
	Calculate Basic Returns of a Price Series
	Uses Formula: (data(t)-data(t-1))-1
	'''
	daily_returns = (data/data.shift(1))-1
	return daily_returns;

def log_returns(data):
	'''
	Calculate Logarithmic Returns of a Price Series
	Uses Formula: ln(data(t)/data(t-1))
	'''
	returns = np.log(data/data.shift(1))
	return returns;

def rolling_volatility(data, n=10):
	'''
	Generate Rolling Standard Deviation of a Series
	n= window size
	'''
	return data.rolling(window=n).std()

def show_data_plot(data):
	'''
	Basic Way to Plot and Show Data
	'''
	data.plot(figsize=(10,5))
	plt.show()

def brownian_motion(mu=0, dt=0.1, N=1000):
	'''
	Generate x-y Brownian Motion Series (Wiener Process)
	mu= mean of distribution
	dt= standard deviation of distribution
	N= size of sample
	'''
	W = scipy.zeros(N+1)
	t = scipy.linspace(0, N, N+1);
	W[1:N+1] = scipy.cumsum(scipy.random.normal(mu,dt,N))
	return t,W

def plot_brownian_motion(t,W):
	'''
	Plots a Wiener Process (Brownian Motion) with Labels and Title
	t= x values (time)
	W= y values (Wiener process)
	'''
	plt.plot(t,W)
	plt.xlabel('Time(t)')
	plt.ylabel('Wiener-process W(t)')
	plt.title('Wiener-process')
	plt.show()

def blackscholes_call(S,E,T,rf,sigma):
	'''
	Prices European Call Option
	S= stock price at current time
	E= strike price in future
	T= expiry in years
	rf= risk free rate (0.n format)
	sigma= volatility of underlying stock
	'''
	d1=(log(S/E)+(rf+sigma*sigma/2.0)*T)/(sigma*sqrt(T))
	d2 = d1-sigma*sqrt(T)
	return S*stats.norm.cdf(d1)-E*exp(-rf*T)*stats.norm.cdf(d2)

def blackscholes_put(S,E,T,rf,sigma):
	'''
	Prices European Put Option
	S= stock price at current time
	E= strike price in future
	T= expiry in years
	rf= risk free rate (0.n format)
	sigma= volatility of underlying stock
	'''
	d1=(log(S/E)+(rf+sigma*sigma/2.0)*T)/(sigma*sqrt(T))
	d2 = d1-sigma*sqrt(T)
	return -S*stats.norm.cdf(-d1)+E*exp(-rf*T)*stats.norm.cdf(-d2)

def zero_bond_price(par_value,market_rate,n):
	'''
	Prices a Zero-Coupon Bond
	par_value= bond's par value (base)
	market_rate= market return rate (0.n format)
	n= years into future
	'''
	return par_value/(1+market_rate)**n
	
def bond_price(par_value,coupon,market_rate,n):
	'''
	Prices a Zero-Coupon Bond
	par_value= bond's par value (base)
	coupon= bond yield (0.n format)
	market_rate= market return rate (0.n format)
	n= years into future
	'''
	c = par_value*coupon
	return c/market_rate*(1-(1/(1+market_rate)**n))+par_value/(1+market_rate)**n
	
def array_to_series(data):
	'''
	Converts numpy.array into pandas.series
	'''
	return pd.Series(data)

def series_to_array(data):
	'''
	Converts pandas.series into numpy.array
	NOTE: Deprecated for Python 3+
	'''
	return data.as_matrix()

def kelly_leverage(returns, rf=0):
	'''
	Calculate Optimal Leverage According to Kelly Formula:
	(meanReturn-rf)/(stdReturn)^2
	returns= returns series
	rf= risk-free rate (0.n format)
	'''
	mean= returns.mean()
	std= returns.std()
	return (mean-rf)/(std**2)

def sharpe_ratio(returns, rf=0):
	'''
	Calculate Basic Sharpe Ratio According to Formula:
	(meanReturn-rf)/(stdReturn)
	returns= returns series
	rf= risk-free rate (0.n format)
	'''
	mean= returns.mean()
	std= returns.std()
	return (mean-rf)/(std)

def kelly_criterion(W=0.5, R=1):
	'''
	Calculate Optimal Portfolio Weight According to Kelly Criterion:
	W= winning probability
	R= win/loss ratio
	'''
	return W- ((1-W)/R)

def ols(Y, X, show_print=True):
	'''
	Runs and fits an Ordinary Least Squares 
	regression on y from x's; including 
	show_print willprint the summary of the regression
	'''
	model= sm.OLS(Y, X)
	results= model.fit()
	if show_print:
		logging.info(results.summary())

	return results
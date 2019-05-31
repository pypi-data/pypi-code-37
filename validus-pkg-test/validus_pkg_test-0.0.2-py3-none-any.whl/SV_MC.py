import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def SIR_Stoch_vol(N,Y,rho,sigma,beta):
    """
    function for estimating parameters for a stochastic volatility model.
    Paramters taken are N the number of paths to simulate, Y the observed returns, T the number of time steps 
    and model parameters to be tested rho, sigma and beta 
    the output is a likelihood value for the give parameters
    
    """
    T = len(Y)
    #initalise matrices to hold values
    SIRMatrix = np.zeros((T,N))
    UnnormalizedWeights = np.zeros((T,N))
    normalizedWeights =  np.zeros((T,N))
    xmean = np.zeros(T)
    xvariance = np.zeros(T)
    x0 = np.random.normal(loc = 0, size = N, scale = np.sqrt((sigma**2)/(1-rho**2)))
    SampledValues = np.zeros((T,N))
    SampledPaths = np.zeros((T,N))
    
    # create Xs and weights
    for i in np.arange(0,T):
        if i==0 :
            w0 = stats.norm.pdf(Y[i],loc = 0, scale = (beta*np.exp(x0/2)))
            SIRMatrix[i,] = x0
            UnnormalizedWeights[i,] = w0
            normalizedWeights[i,] = UnnormalizedWeights[i,]/sum(UnnormalizedWeights[i,])
            
        else:
            SIRMatrix[i,] = np.random.normal(size = N,loc = rho * SIRMatrix[i-1,],scale = sigma)
            
            UnnormalizedWeights[i,] = stats.norm.pdf(Y[i],loc = 0, scale = (beta*np.exp(SIRMatrix[i,]/2)))
            normalizedWeights[i,] = UnnormalizedWeights[i,]/sum(UnnormalizedWeights[i,])
    # sample path indexes according to normalized weights
        Sampled_indexes = np.random.choice(np.arange(0,N),size = N, replace= True, p = normalizedWeights[i,])
    # store values sampled
        SIRMatrix[i,] = SIRMatrix[i,Sampled_indexes]
        
     # store paths sampled    
        SampledPaths[0:i,] = SIRMatrix[0:i,Sampled_indexes]
        
    ## calcuate mean and variance
        xmean[i] = np.mean(SIRMatrix[i,])
        xvariance[i] = np.mean(SIRMatrix[i,]**2)-xmean[i]**2
        
    likelihood = np.cumsum(np.log(np.mean(UnnormalizedWeights,axis=1)))
    
    return [xmean , xvariance, likelihood, SampledValues]



### this method is poor and inefficient there are many ways to imporve it such as SGD but this also comes with issues
def maximum_like(rho_len,sigma_len,N,Y):
    MLE = np.zeros((rho_len,sigma_len))
    rhogrid = np.linspace(-0.99,0.99,rho_len)
    sigmagrid = np.linspace(0.01,3,sigma_len)
    for i in np.arange(0,rho_len):
        for j in np.arange(0,sigma_len):
                current_run = SIR_Stoch_vol(N,Y,rho=rhogrid[i],beta=1,sigma=sigmagrid[j])
                MLE[i,j] = current_run[2][len(Y)-1]
                
                
    k = np.where(MLE==MLE.max())
    k=[k[0][0],k[1][0]]
    
    return {'rho' : rhogrid[k[0]],'sigma' : sigmagrid[k[1]]}
    

def stochastic_volatility_run(N,T,beta,rho,sigma,x0):
    vol = np.zeros((T,N))
    ret = np.zeros((T,N))
    
    for i in np.arange(0,T):
            if i ==0:
                vol[i,]= x0
                ret[i,] = beta * np.exp(vol[i,]/2) * np.random.normal(size = N, loc= 0, scale = 1)
            else:
                vol[i,] = rho*vol[i-1,]  +  sigma*np.random.normal(size = N, loc= 0, scale = 1)
                ret[i,] = beta * np.exp(vol[i,]/2) *np.random.normal(size = N, loc= 0, scale = 1)
                
    return np.median(vol,axis=1)


def vol_curve(v):
    """
    function takes values of volatility over time and returns percentage movements based on the lower 95% CI band
    """
    #split data into monthly buckets
    f =v[::21]
    # come up with a time adjustment
    t = np.sqrt(np.arange(21,len(f)*21+21,21))
    #calulate lower bound 
    l = np.exp(f/2)*t*1.96
    # return % move
    return 1-l/100


    
    
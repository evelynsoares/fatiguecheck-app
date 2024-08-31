import numpy as np

def sigmaa(yb,T,EI,dal,Eal):
    p=(T/EI)**0.5
    K=float(Eal*dal*(p**2)/(4*((np.exp(-p*89))-1+p*89)))
    sa=K*yb
    return sa
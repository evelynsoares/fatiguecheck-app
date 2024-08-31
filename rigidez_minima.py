import numpy as np

def rigidez_minima(nal,dal,na,da):
    Eal=69000 #valor em MPa
    Ea=200000 #valor em MPa
    EI=(na*Ea*np.pi*(da**4)/64)+(nal*Eal*np.pi*(dal**4)/64)
    return EI
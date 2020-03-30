import math
import numpy as np
import scipy.stats as st

def HW(v):
    return sum( [int(v)&(1<<i)>0 for i in range(len(bin(int(v))) - 2)])

def normpdf(x, mean, sd):
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def HW_leakage(val, sigma, size):
    l = st.norm.rvs(loc = HW(val), scale = sigma)
    p = np.asarray([normpdf(l, HW(i), sigma) for i in range(size)])
    return(p/sum(p))

def MI_register(sigma):
    return (0.5 * math.log2((2.0/(sigma**2)) + 1) * 0.125)

def MI_carry(sigma):
    return (0.5 * math.log2((0.5/(sigma**2)) + 1) * 0.125)

a = np.zeros(32)
a[31] = 107
a[30] = 23  
a[29] = 209 
a[28] = 242 
a[27] = 225
a[26] = 44 
a[25] = 66
a[24] = 71
a[23] = 248
a[22] = 188
a[21] = 230
a[20] = 229
a[19] = 99
a[18] = 164
a[17] = 64
a[16] = 242
a[15] = 119
a[14] = 3
a[13] = 125
a[12] = 129
a[11] = 45
a[10] = 235
a[9] = 51
a[8] = 160
a[7] = 244
a[6] = 161
a[5] = 57
a[4] = 69
a[3] = 216
a[2] = 152
a[1] = 194
a[0] = 150
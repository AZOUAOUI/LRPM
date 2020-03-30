import random as rand
from modelsumproduct import *

def build_fg_binit_full(rs, debug=False):
    
    vs = 2**rs
    a30 = 23 % vs
    a31 = 107 % vs
    
    node_names = ['b0', 'b1', 'c30', 'acc00', 'acc10', 'carry0', 'R00', 'R01', 'acc11', 'carry_acc12', 'R10', 'R11',
              'c31', 'carry2', 'acc20', 'carry3', 'acc21', 'R20', 'R21', 'c32', 'carry4', 'c33', 'carry_acc31']

    variables = dict() 
    for i in range(len(node_names)):
        variables[node_names[i]] =  Variable(node_names[i], 1)
    
    ################# 
    
    factors = dict()

    factors['fmul030'] = Mul('fmul030', a30)
    factors['fmul031'] = Mul('fmul031', a31)
    factors['fmul130'] = Mul('fmul130', a30)
    factors['fmul131'] = Mul('fmul131', a31)
    
    factors['fadd0'] = Add('fadd0')
    factors['fadd1'] = Add('fadd1')
    factors['fadd2'] = Add('fadd2')
    
    factors['fadc0w0'] = Adc_w0('fadc0w0')
    
    factors['fadc0'] = Adc('fadc0')
    factors['fadc1'] = Adc('fadc1')
    
    factors['fadd0carries'] = Add_carries('fadd0carries')
    
    ################
    
    g = FactorGraph(debug=debug)
    for v in variables:
        g.add(variables[v])
    for f in factors:
        g.add(factors[f])
        
    g.connect('fmul030','b0')
    g.connect('fmul030','c30')
    g.connect('fmul030','acc00')
    
    g.connect('fmul031','b0')
    g.connect('fmul031','R10')
    g.connect('fmul031','R11')
    
    g.connect('fmul130','b1')
    g.connect('fmul130','R00')
    g.connect('fmul130','R01')
    
    g.connect('fmul131','b1')
    g.connect('fmul131','R20')
    g.connect('fmul131','R21')
    
    g.connect('fadd0','acc00')
    g.connect('fadd0','R00')
    g.connect('fadd0','acc10')
    g.connect('fadd0','carry0')
    
    g.connect('fadd1','acc10')
    g.connect('fadd1','R10')
    g.connect('fadd1','c31')
    g.connect('fadd1','carry2')
    
    g.connect('fadd2','acc20')
    g.connect('fadd2','R20')
    g.connect('fadd2','c32')
    g.connect('fadd2','carry4')
    
    g.connect('fadc0w0','R01')
    g.connect('fadc0w0','carry0')
    g.connect('fadc0w0','acc11')
    g.connect('fadc0w0','carry_acc12')
    
    g.connect('fadc0','acc11')
    g.connect('fadc0','R11')
    g.connect('fadc0','carry2')
    g.connect('fadc0','acc20')
    g.connect('fadc0','carry3')
    
    g.connect('fadc1','acc21')
    g.connect('fadc1','R21')
    g.connect('fadc1','carry4')
    g.connect('fadc1','c33')
    g.connect('fadc1','carry_acc31')
    
    g.connect('fadd0carries','carry_acc12')
    g.connect('fadd0carries','carry3')
    g.connect('fadd0carries','acc21')
    
    return g
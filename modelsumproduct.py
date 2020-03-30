import numpy as np
import math
from utility import *


"""
This is the implementation of the BP approximation model
"""
class Node:
    def __init__(self, name):
        self.connections = []
        self.inbox = {}
        self.name = name

    def append(self, to_node):
        self.connections.append(to_node)
        to_node.connections.append(self)

    def deliver(self, step_num, mu):
        """
    Ensures that inbox is keyed by a step number
    """
        if self.inbox.get(step_num):
            self.inbox[step_num].append(mu)
        else:
            self.inbox[step_num] = [mu]


class Factor(Node):
    """
  NOTE: For the Factor nodes in the graph, it will be assumed
  that the connections are created in the same exact order
  as the factor function parameters are given
  """
    def __init__(self, name):
        Node.__init__(self, name)
  
    
class Leakage_factor(Factor):
    def __init__(self, name, potentials):
        self.p = potentials 
        Node.__init__(self, name)
    
    def make_message(self, recipient):
        return self.p


class Mov(Factor):
    def __init__(self, name):
        Factor.__init__(self, name) 
        
    def make_message(self, recipient):
        recipient_index = self.connections.index(recipient)
        unfiltered_mus = self.inbox[max(self.inbox.keys())]
        val = next(mu for mu in unfiltered_mus if not mu.from_node == recipient).val
        if (val >1):
            return 1
        return val
    
    
class Mul(Factor):
    def __init__(self, name, a):
        self.a = a 
        Factor.__init__(self, name)
        
    def make_message(self, recipient):
        recipient_index = self.connections.index(recipient)
        unfiltered_mus = self.inbox[max(self.inbox.keys())]
        
        mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[0]).val
        muj = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[1]).val
        muk = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[2]).val
        
        val = 0.0
        
        if(recipient_index == 2):
            val = mui
        
        if(recipient_index == 1):
            val = mui 
                
        if(recipient_index == 0):
            val = 0.5 *(muj + muk)
       
        if(val>1):
            val = 1
            
        return val
    
    
class Add_nocarry(Factor):
    def __init__(self, name):
        Factor.__init__(self, name)
    
    def make_message(self, recipient):
        recipient_index = self.connections.index(recipient)
        unfiltered_mus = self.inbox[max(self.inbox.keys())]
        
        mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[0]).val
        muj = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[1]).val
        muk = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[2]).val
        
        val = 0.0
        
        if(recipient_index == 2):
            val = mui * muj
            
        if(recipient_index == 0):
            val = muj * muk
                    
        if(recipient_index == 1):
            val = mui * muk
            
        val = 0.6 * val
        
        if(val>1):
            val = 1
            
        return val
    

class Adc_w0_nocarry(Factor):
    def __init__(self, name):
        Factor.__init__(self, name)
    
    def make_message(self, recipient):
        recipient_index = self.connections.index(recipient)
        unfiltered_mus = self.inbox[max(self.inbox.keys())]
        
        mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[0]).val
        muj = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[1]).val
        
        val = 0.0
        
        if(recipient_index == 1):
            val = mui
            
        if(recipient_index == 0):
            val = muj
        
        val = 0.7 * val
        
        if(val>1):
            val = 1
            
        return val
    

class Adc_nocarry(Factor):
    def __init__(self, name):
        Factor.__init__(self, name)
    
    def make_message(self, recipient):
        recipient_index = self.connections.index(recipient)
        unfiltered_mus = self.inbox[max(self.inbox.keys())]
        
        mui = mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[0]).val
        muj = mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[1]).val
        muk = mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[2]).val
        
        val = 0.0
        
        if(recipient_index == 2):
            val = mui * muj
        
        if(recipient_index == 0):
            val = muj * muk
                    
        if(recipient_index == 1):
            val = mui * muk
            
        val = 0.6 * val
        
        if(val>1):
            val = 1
            
        return val
    

class Add(Factor):
    def __init__(self, name):
        Factor.__init__(self, name)
    
    def make_message(self, recipient):
        recipient_index = self.connections.index(recipient)
        unfiltered_mus = self.inbox[max(self.inbox.keys())]
        
        mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[0]).val
        muj = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[1]).val
        muk = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[2]).val
        mul = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[3]).val
        
        val = 0.0
        
        if(recipient_index == 2):
            val = 0.8 * mui * muj
        
        if(recipient_index == 3):
            val =  0.35 * mui * muj  #0.125
         
        if(recipient_index == 0):
            val = 0.65 * muj *( muk + mul )
        
        if(recipient_index == 1):
            val = 0.65 * mui * ( muk + mul )
        
        if(val>1):
            val = 1
            
        return val
    
    
class Adc_w0(Factor):
    def __init__(self, name):
        Factor.__init__(self, name)
    
    def make_message(self, recipient):
        recipient_index = self.connections.index(recipient)
        unfiltered_mus = self.inbox[max(self.inbox.keys())]
        
        mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[0]).val
        muj = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[1]).val
        muk = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[2]).val
        mul = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[3]).val
        
        val = 0.0
        
        if(recipient_index == 2):
            val = mui * muj

        if(recipient_index == 3):
            val =  mui * muj  # 0.125
               
        if(recipient_index == 0):
            val = muj * (muk + mul)
               
        if(recipient_index == 1):
            val = mui * (muk + mul) # 0.125
        
        if(val>1):
            val = 1
        return val
    
    
class Adc(Factor):
    def __init__(self, name):
        Factor.__init__(self, name)
    
    def make_message(self, recipient):
        recipient_index = self.connections.index(recipient)
        unfiltered_mus = self.inbox[max(self.inbox.keys())]
        
        mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[0]).val
        muj = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[1]).val
        muk = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[2]).val
        mul = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[3]).val
        mum = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[4]).val
        
        val = 0.0
        
        if(recipient_index == 3):
            val = mui * muj * muk
                    
        if(recipient_index == 4):
            val =  mui * muj * muk #0.125
                        
        if(recipient_index == 0):
            val = 0.9 * muj * muk * (mul + mum)
        
        if(recipient_index == 1):
            val = 0.9 * mui * muk * (mul + mum)
                        
        if(recipient_index == 2):
            val = 0.1 * mui * muj * (mul + mum) #0.125
            
        if(val>1):
            val = 1
            
        return val
    
class Add_carries(Factor):
    def __init__(self, name):
        Factor.__init__(self, name)
    
    def make_message(self, recipient):
        recipient_index = self.connections.index(recipient)
        unfiltered_mus = self.inbox[max(self.inbox.keys())]
        
        mui = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[0]).val
        muj = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[1]).val
        muk = next(mu for mu in unfiltered_mus if mu.from_node == self.connections[2]).val
               
        val = 0.0
        
        if(recipient_index == 2):
            val = mui * muj
        
        if(recipient_index == 0):
            val = muj * muk
                   
        if(recipient_index == 1):
            val = mui * muk
            
        if(val>1):
            val = 1
            
        return val
    
    
    
class Variable(Node):
    def __init__(self, name, size, value=-1):
        self.bfmarginal = None
        self.size = size
        self.value = value
        assert value < size
        Node.__init__(self, name)

    def marginal(self):
        if len(self.inbox):
            mus = self.inbox[max(self.inbox.keys())]
            s = 0.0 
            for mu in mus:
                s += mu.val
            if s > 1:
                s = 1
            return s
        else:
            return 1 

    def make_message(self, recipient):
        if not len(self.connections) == 1:
            unfiltered_mus = self.inbox[max(self.inbox.keys())]
            mus = [mu for mu in unfiltered_mus
                   if not mu.from_node == recipient]
            s = 0.0 
            for mu in mus:
                s += mu.val
            if s > 1:
                s = 1
            return s
        else:
            return 1


class Mu:
    def __init__(self, from_node, val):
        self.from_node = from_node
        self.val = val
        

class FactorGraph:
    def __init__(self, first_node=None, debug=False):
        self.nodes = {}
        self.debug = debug
        if first_node:
            self.nodes[first_node.name] = first_node

    def add(self, node):
        assert node not in self.nodes
        self.nodes[node.name] = node

    def connect(self, name1, name2):
        self.nodes[name1].append(self.nodes[name2])

    def append(self, from_node_name, to_node):
        assert from_node_name in self.nodes
        tnn = to_node.name
        # add the to_node to the graph if it is not already there
        if not (self.nodes.get(tnn, 0)):
            self.nodes[tnn] = to_node
        self.nodes[from_node_name].append(self.nodes[tnn])
        return self

    def leaf_nodes(self):
        return [node for node in self.nodes.values()
                if len(node.connections) == 1]

    def export_marginals(self):
        return dict([
            (n.name, n.marginal()) for n in self.nodes.values()
            if isinstance(n, Variable)
        ])

    @staticmethod
    def compare_marginals(m1, m2):
        assert not len(np.setdiff1d(m1.keys(), m2.keys()))
        s = 0.0 
        for k in m1.keys():
            s += abs(m1[k] - m2[k])
        return s
    

    def compute_marginals(self, max_iter=500, tolerance=1e-6):
        
        epsilons = [1]
        step = 0

        for node in self.nodes.values():
            node.inbox.clear()

        cur_marginals = self.export_marginals()

        for node in self.nodes.values():
            if isinstance(node, Variable):
                message = Mu(node, np.ones(node.size))
                for recipient in node.connections:
                    recipient.deliver(step, message)
                    
        factors = [n for n in self.nodes.values() if isinstance(n, Factor)]
        variables = [n for n in self.nodes.values() if isinstance(n, Variable)]
        senders = factors + variables
        
        while (step < max_iter):# and tolerance < epsilons[-1]:
            
            last_marginals = cur_marginals
            step += 1
            
            for sender in senders:
                next_recipients = sender.connections
                for recipient in next_recipients:
                    if self.debug:
                        print(sender.name + ' -> ' + recipient.name)
                    val = sender.make_message(recipient)
                    message = Mu(sender, val)
                    recipient.deliver(step, message)
        
            for sender in senders:
                if (step - 1) in sender.inbox:
                    del sender.inbox[step-1]
            
            cur_marginals = self.export_marginals()
            epsilons.append(self.compare_marginals(cur_marginals, last_marginals))
            
        return epsilons[1:]
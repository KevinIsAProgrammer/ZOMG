#!/bin/python3

from my_io import IO 
from mem import Mem
from pickle import dump,load

class ZOMG(object):
    """
    Usage: from zomg import ZOMG
    vm = ZOMG(size)

    // enter a ZOMG program
    vm.m[address] = True / False
    ...
    // run a ZOMG program
    vm.c = <start address>
    vm.step() / vm.run()
    """
    def __init__(self, size):
        self.m = Mem(size)
        self.io = IO()
        self.f = False # Fixed addressing mode (False for relative, True for fixed)

        self.c = 0
        self.d = 0

        self.v = 0
        self.u = True  # Unset Sign? (True if sign hasn't been set, False otherwise)
        self.s = True  # Sign of n (True for positive, False for negative)

        self.debug=True # start running in debug mode

    def __repr__(self):
        return (repr(self.m) + "\n" +
                "f="+repr(self.f) +"\n" +
                "c="+repr(self.c) +"\n" +
                "d="+repr(self.d) +"\n" +
                "n="+self.sign()+repr(self.v)+"\n") 

    def n(self):
        if self.s:
           return self.v
        else:
           return -1 * self.v

    def sign(self):
        if self.s:
           return "+"
        else:
           return "-"

    def clear_n(self):
        self.u = True
        self.s = True 
        self.v = 0 

    def step(self):
        if self.c < 0:
           self.invalid(self.c)
        symbol= self.m.symbol(self.c)
        set_c = self.handle_symbol(symbol)
        if set_c:
           self.c +=2

    def run(self):
        self.run=True
        while(self.run):
              self.step()

    def invalid(self, address):
        self.show("Invalid address:" + address)
        self.run=False    

    def exit(self,code):
        self.show("exit("+str(code)+")") 
        self.run=False

    def handle_symbol(self, symbol):
        self.show("Handling " + str(symbol))
        if symbol == "0":
           return self.zero()
        elif symbol == "1":
           return self.one()
        elif symbol == "#":
           return self.math()
        elif symbol == "?":
           return self.go()  
        raise Hell  

    def zero(self): 
        if self.u:
           self.s = True 
           self.u = False 
        else:
           self.v *= 2
        return True

    def one(self):
        if self.u:
           self.s = False 
           self.u = False
        else:
           self.v *=2
           self.v +=1
        return True 

    def math(self):
        if not(self.s) and self.v == 0:  # n == -0
           self.d = self.c
        elif self.v == 0:              # n == 0
           self.d = 0
        else: 
           self.d += self.n()
        self.clear_n()
        return True 

    def go(self):
        if not(self.s) and self.v==0:		# -0 sets fixed addressing
           self.show("Set fixed addressing")
           self.f = True 
           self.clear_n()
           return True 
        elif self.f and self.s and self.v == 0: # +0 sets relative from fixed 
           self.show("Set relative addressing")
           self.f = True
           self.clear_n()
           return True
        elif self.f and not(self.s):		# -n in fixed mode exits
             self.exit(self.v-1)
             self.clear_n() 
             return True
        
        if self.d == 0:
           self.do_io(self.m.mem[0:8]) 
           b = False
        else: 
           b = self.m.flip(self.d) 
           self.show("d="+str(self.d))
           self.show("Result of flip was:" + str(b)) 
        if b:
           self.show("Branch was true")
           if self.f:
              self.show("Branch to fixed offset"+str(self.n()))
              self.c = self.n()
           else:      
              self.show("Branch to relative offset"+str(2*self.n()))
              self.c += 2 * self.n()
           self.clear_n()
           return False
        else:
           self.show("Branch was false")
           self.clear_n()
           return True

    def do_io(self, bits):
        self.show("I/O", bits)
        result = self.io.do_io(bits)
        self.show("Result", result)
        self.m.mem[0:8] = result

    def save(self, name, start, end):
        f=open(name,"wb")
        dump(self.m.mem[start:end],f)
        f.close()

    def load(self, name, start):
        f=open(name,"rb")
        program = load(f)
        self.m.mem = self.m.mem[0:start]+program+self.m.mem[start+len(program):]
        self.c = start

    def clear(self):
        self.m.mem.clear()
        self.f=False
        self.c = 0
        self.d = 0
        self.clear_n()
        
    def code(self):
        return self.m.code()

    def show(self, *msg, **kw):
        if self.debug:
            print(*msg, **kw)


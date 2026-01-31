#!/bin/python3
import pickle

class Symbol(object):
     def __init__(self, b1, b2):
          self.b1 = b1
          self.b2 = b2

     def __str__(self):
          if self.b1:
            if self.b2:
              return "?"
            else:
              return "#"
          else:
            if self.b2:
               return "1"
            else:
               return "0"

     def __repr__(self):
          return str(self)

     def __eq__(self, other):
          return str(self) == str(other)

class Mem(object):
     def __init__(self, size):
          self.mem = [False] * size
          self.size = size

     def __repr__(self):
         return self.data()

     def code(self):
         s=""
         for i in range(0, self.size, 2):
             s += str(self.symbol(i))
         return s

     def data(self):
         s=""
         for i in range(0,self.size,2):
               s+=self.at(i)+self.at(i+1)+ " "
         return s

     def bit(self,bool):
         if (bool):
            return "1"
         return "0"

     def symbol(self, address):
         b1 = self.mem[address]
         b2 = self.mem[address + 1]
         return Symbol(b1,b2)

     def flip(self, address):
         if address >= self.size:
             return False
         if address < 0: 
             return True
         b1 = self.mem[address]
         self.mem[address] = not(b1)
         return self.mem[address] 

     def at(self,address):
         return self.bit(self.at_(address))

     def at_(self, address):
         if (address >= self.size):
             return False
         elif address > 0:
            return self.mem[address]
         elif address == 0:
            return False
         else:
            return True 

     def readFile(self, name, address=8):

         pos = address
         handle=open(name,"rb")

         data=handle.read()
         for b in data:
            for shift in range(7,-1,-1):
                self.mem[pos] = (b >> shift & 1) == 1 
                pos += 1

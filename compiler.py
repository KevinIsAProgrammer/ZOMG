#!/usr/bin/python

import os

byte=0
shift=6
while True:
    try:
        b=os.read(0,1) 
    except OSError:
        print("Can't read")
        exit(1)

    if b == b'':
        break

    if b == b'0':
        # don't bother to or with zero
        shift -=2
        os.write(2, b)
    elif b == b'1':
        byte = byte | (1 << shift)
        shift -= 2
        os.write(2, b)
    elif b == b'#':
        byte = byte | (2 << shift)
        shift -= 2
        os.write(2, b)
    elif b == b'?':
        byte = byte | (3 << shift)
        shift -= 2
        os.write(2, b)

    if shift < 0:
        os.write(1, byte.to_bytes())
        shift=6
        byte=0
os.write(1, byte.to_bytes())

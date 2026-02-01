from sys import argv
from zomg import ZOMG

vm=ZOMG(256)
if len(argv) < 2:
	print("Usage: python run <file.z>")
	exit(0)
vm.m.readFile(argv[1])
vm.debug=False
vm.c=8
vm.run()

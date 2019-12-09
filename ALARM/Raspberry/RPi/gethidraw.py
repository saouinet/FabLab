#!/usr/bin/python3

if __name__ == "__main__":
	f=open("/dev/input/event1","rb")
	while 1 : 
		data = f.read(10)
		print(data)

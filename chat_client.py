#!/usr/bin/env python3
import socket as sock
import time
import threading
from select import select

TARGET_IP = "localhost"
TARGET_PORT = 13131

s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
s.connect((TARGET_IP, TARGET_PORT))

def sender():
	try:
		message = None
		while True:
			message = input("> ")
			#time.sleep(0.2)
			if message in ["end", "bye", "q"]:
				break
			s.sendall(message.encode("ascii"))

	except Exception as e:
		print(e)
		s.close()
	finally:
		s.close()

def listener():
	try:
		while mouth.isAlive():
			s.setblocking(0)

			ready = select([s], [], [], 5) # seconds
			if ready[0]:
				incoming = s.recv(1024)
				print(incoming.decode("ascii"), end="")
				print("\n> ", sep="", end="")
			#time.sleep(2)

	except Exception as e:
		s.close()
		print(e)

mouth = threading.Thread(target=sender)
ears = threading.Thread(target=listener)

mouth.start()
ears.start()
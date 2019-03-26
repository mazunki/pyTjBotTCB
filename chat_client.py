#!/usr/bin/env python3
import socket as sock
import time
import threading
from select import select

TARGET_IP = "srv.circuitbreakers.tech"
TARGET_PORT = 13131

MY_NAME = None

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
		global MY_NAME
		if MY_NAME == None:
			incoming = s.recv(1024).decode("ascii")
			if "set_name " in incoming:
				MY_NAME = incoming.replace("set_name ", "")
				print("my name is", MY_NAME)
			else:
				print("<== Warning. Client has no name. ==>")
		else:
			print(MY_NAME)

		while mouth.isAlive():
			s.setblocking(0)
			ready = select([s], [], [], 5) # seconds
			if ready[0]:
				incoming = s.recv(1024)
				print(incoming.decode("ascii"), end="")
				print("\n> ", sep="", end="")

				network_parser(incoming.decode("ascii"))

			#time.sleep(2)

	except Exception as e:
		s.close()
		print(e)

def network_parser(text_to_parse):
	
	start_of_message = text_to_parse.find(":") # "('127.12.34.56', 34278): hello world!!

	try:
		assert start_of_message != -1  # Invalid

		source = text_to_parse[:start_of_message]  # "('127.12.34.56', 34278)"
		assert source[0] == "(" and source[-1] == ")"

		source = source[1:-1]  # "'127.12.34.56', 34278"

		conn = source.split(", ")  # ["'127.12.34.56'", "34278"]
		conn_ip = conn[0].replace("'","").replace('"','')  # "127.12.34.56"
		conn_port = int(conn[1])  # 24278
		conn = (conn_ip, conn_port) # cleaned up

		message = text_to_parse[start_of_message+2:]  # ignoring the space

		tuplified_msg = tuple(message.split(" "))  # oh god this can't be a good idea

		if tuplified_msg[0] == MY_NAME:
			pass

	except AssertionError:
		return


mouth = threading.Thread(target=sender)
ears = threading.Thread(target=listener)

mouth.start()
ears.start()
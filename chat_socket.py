#!/usr/bin/env python3
import socket as sock
import threading

LOCAL_IP = "localhost"
LOCAL_PORT = 13131

NAMES = ["bob", "maria", "tom", "apple"]

s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
s.bind((LOCAL_IP, LOCAL_PORT))

s.listen(True)

max_attempts = 3
attempts = 0

def new_connection(conn, conn_ip):
	print("found new client:", conn_ip)
	global NAMES
	assigning_name = NAMES.pop(0)
	name_set = "set_name "+assigning_name
	conn.sendall(name_set.encode("ascii"))
	print("set", assigning_name, "to", conn)
	try:
		while True:
			try:
				income = b""
				income = conn.recv(1024)
				print("{}: {}".format(conn_ip, income.decode("ascii")))
				if income != b"":
					global connections
					others = [client for client in connections if client[1] != conn_ip]
					# print(others)
					for client in others:
						print(client[1])
						print("sending {} to {}".format(income, client))
						stream_msg = str(conn_ip) + ": " + income.decode("ascii") 
						client[0].sendall(stream_msg.encode("ascii"))
					income = b""
				else:
					print("{}: <empty>".format(conn_ip))
					conn.close()
					connections.remove([conn, conn_ip])
					return		

			except Exception as e:
				print(e)
				conn.close()
	except Exception as e:
		print(e)
		conn.close()


connections = list()

while attempts < max_attempts:
	conn, conn_ip = s.accept()

	try:
		connections.append([conn, conn_ip])
		conn_thread = threading.Thread(target=new_connection, args=(conn, conn_ip))
		conn_thread.start()
	except Exception as e:
		print(e)
	finally:
		attempts += 1
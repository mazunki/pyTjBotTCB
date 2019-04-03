#!/usr/bin/env python3
"""
Used by the server.
"""
import socket as sock
import threading


LOCAL_IP = "192.168.1.234"
LOCAL_PORT = 13131

NAMES = ["bob", "maria", "tom", "apple"]  # samples
current_connections = dict()

s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
s.bind((LOCAL_IP, LOCAL_PORT))

s.listen(True)

MAX_ATTEMPTS = 3
ATTEMPTS = 0

def set_name(conn, conn_ip, name=None):
	"""
	Similar to a DNS service, pretty much.
	"""
	print("found new client:", conn_ip)
	if name == None:	
		global NAMES
		assigning_name = NAMES.pop(0)
	else:
		assigning_name = name
	name_set = "set_name "+assigning_name
	conn.sendall(name_set.encode("ascii"))

	global current_connections
	current_connections_ = current_connections.copy()  # python is a baby who is afraid of things changing size
	for pre_names, pre_conns in current_connections_.items():
		if pre_conns == [conn_ip, conn]:
			del current_connections[pre_names]
		if pre_names == name:
			return False  # name is in use already! this causes changing to self's old name not being allowed but welp

	current_connections[assigning_name] = [conn_ip, conn]

	return assigning_name


def close_session(conn, conn_ip):
	"""
	Actually not functional, per default behaviour, as clients already close their session from their side.
	"""
	try:
		conn.close()
		current_connections.pop(conn_ip)
		print("<== Closed session {} ==>".format(conn_ip))
	except Exception as e:
		print("<== Couldn't close session on {} ==>: {}".format(conn_ip, e))
		return False
	finally:
		return True

def broadcast(msg, src_ip, src_conn=None, exclude_self=True):  # src_conn required if sending in return too 
	global current_connections
	others = [client[1] for client in current_connections.values() if client[0] != src_ip]  # client = [conn, src_ip]
	
	print(current_connections)
	for src_name, location in current_connections.items():
		if location[0] == src_ip:
			whomstve = src_name
	stream_msg = str(whomstve) + ": " + msg.decode("ascii")

	for client in others:
		client.sendall(stream_msg.encode("ascii"))
	if not exclude_self:
		src_conn.sendall(stream_msg.encode("ascii"))


def new_connection(conn, conn_ip):
	host_name = set_name(conn, conn_ip)  # also adds to connection host list
	if host_name:
		print("set", host_name, "to", conn)
	else:
		print("couldnt set name")

	try:
		while True:
			try:
				income = b""
				income = conn.recv(1024)
				print("{}: {}".format(conn_ip, income))

				if "set name" in income.decode("ascii"):
					host_name = set_name(conn, conn_ip, name=income.decode("ascii")[income.decode("ascii").find("my name is")+len("my name is"):])
					if host_name:
						print("set", host_name, "to", conn)
					else:
						print("couldn't set name")

				elif income not in [b"q", b"end", b"bye", b""]:
					broadcast(income, conn_ip)

				else:
					print("{}: <end message>".format(conn_ip))
					close_session(conn, conn_ip)
					return

			except Exception as e:
				print(e)
				close_session(conn, conn_ip)
				return

	except Exception as e:
		print(e)
		close_session(conn, conn_ip)

threads = list()
try:
	while ATTEMPTS < MAX_ATTEMPTS:
		conn, conn_ip = s.accept()

		try:
			conn_thread = threading.Thread(target=new_connection, args=(conn, conn_ip))
			# threads.append(conn_thread)
			conn_thread.start()
		except Exception as e:
			print(e)
			s.close()
		finally:
			ATTEMPTS += 1
except:
	for connection in current_connections:
		close_session(connection)
finally:
	for connection in current_connections:
		close_session(connection)
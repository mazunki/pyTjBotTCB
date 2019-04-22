#!/usr/bin/env python3
import socket as sock
import time
import threading
from select import select  # permits timeout/readychecks
if __name__ == '__main__':
	import sys
	sys.path.insert(0, "..")
import audio.audioout
import watson.tts
import text_handler

TARGET_IP = "srv.circuitbreakers.tech"
TARGET_PORT = 13131

MY_NAME = None

s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
s.connect((TARGET_IP, TARGET_PORT))

def request_name(name):
    name_command = "set name " + name
    s.sendall(name_command.encode("ascii"))


def sender():
    try:
        message = None
        while True:
            message = input("> ")
            #time.sleep(0.2)
            if message in ["end", "bye", "q"]:
                break

            elif "my name is" in message:
                request_name(message[message.find("my name is")+len("my name is")+1:])

            else:
                s.sendall(message.encode("ascii"))

    except Exception as e:
        print(e)
        s.close()
        return
    finally:
        s.close()
        return

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
                incoming = s.recv(1024).decode("ascii")
                if incoming != "":
                    print(incoming, end="")
                    print("\n> ", sep="", end="")

                    if "set_name " in incoming:
                        MY_NAME = incoming.replace("set_name ", "")
                        print("my name is", MY_NAME)

                    else:
                        network_parser(incoming)

    except Exception as e:
        s.close()
        print(e)

def network_parser(text_to_parse):
	
    start_of_message = text_to_parse.find(":") # "('127.12.34.56', 34278): hello world!!

    try:
        assert start_of_message != -1  # Invalid

        if MY_NAME == None:
            source = text_to_parse[:start_of_message]  # "('127.12.34.56', 34278)"
            assert source[0] == "(" and source[-1] == ")"

            source = source[1:-1]  # "'127.12.34.56', 34278"

            conn = source.split(", ")  # ["'127.12.34.56'", "34278"]
            conn_ip = conn[0].replace("'","").replace('"','')  # "127.12.34.56"
            conn_port = int(conn[1])  # 24278
            conn = (conn_ip, conn_port) # cleaned up

            message = text_to_parse[start_of_message+2:]  # ignoring the space

            tuplified_msg = tuple(message.split(" "))  # oh god this can't be a good idea

        else:
            message = text_to_parse[start_of_message+2:]
            tuplified_msg = tuple(message.split(" "))

            if tuplified_msg[0] == MY_NAME:
                try:
                    assert len(tuplified_msg) >= 2
                except AssertionError:
                    return
                text_handler.do_stuff(" ".join(tuplified_msg[1:]))

            elif tuplified_msg[0] == "tell":
                try:
                    assert len(tuplified_msg) >= 3
                except AssertionError:
                    return
            if tuplified_msg[1] == MY_NAME:
                text_handler.do_stuff(" ".join(tuplified_msg[2:]))


    except AssertionError:
        return

def go_online():
    global mouth
    global ears

    mouth = threading.Thread(target=sender)
    ears = threading.Thread(target=listener)

    mouth.start()
    ears.start()

if __name__ == '__main__':
    go_online()

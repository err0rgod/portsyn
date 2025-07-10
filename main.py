import argparse
import socket

ip=input("Enter The IP adresss")
p=int(input("Enter the port number"))


for port in p:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout()
    result = s.connect_ex((ip,port))

    if result == 0:
        print(f"the {port} is Open")
    s.close




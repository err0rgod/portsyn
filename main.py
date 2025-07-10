import argparse
import socket

tar=input("Enter the target")
p=int(input("Enter the port number"))


for port in p:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout()
    result = s.connect_ex((tar,port))

    if result == 0:
        print(f"the {port} is Open")
    s.close




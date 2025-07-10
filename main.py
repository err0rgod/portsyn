import argparse
import socket

tar=input("Enter the target: ")
p=int(input("Enter the port number: "))
ports = range(1,p)


for port in ports:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((tar,port))

    if result == 0:
        print(f"the port {port} is Open")
    else:
        print(f"port {port} not open. Failure.")
    s.close
    




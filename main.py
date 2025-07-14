import argparse
import socket
import threading
import socks
#from urllib.request import proxyhandler , build_opener
from itertools import cycle

tar="steminfinity.in"#input("Enter the target: ")
p=50#int(input("Enter the port number: "))
t=30#int(input("Enter number of threads: "))
ports = range(1,p)

open_ports= []
serv_dtc = []


USE_PROXY = True  # Toggle proxy on/off

proxy_ip = "185.59.100.55"
proxy_port = 1080


#proxy_pool = cycle(PROXY)


def port_scan(tar,port):
    try:
        if USE_PROXY:
            socks.set_default_proxy(socks.SOCKS5, proxy_ip, 1080)
            socket.socket = socks.socksocket
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((tar,port))

        if result == 0 :
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            ser=service_detect(port)
            banner = grab_ban(s)
            print(f"[+] Port {port} is open : {ser}  :  {banner[:50]}", end='\r')
            open_ports.append(port)
            serv_dtc.append((ser,banner))
        else:
            print(f"port {port} not open. Failure.")
        s.close()
    
    except Exception as e:
        print(f"Error while scanning port {port} {e}")



def multi_threading(tar,ports,max_threads=10):
    threads = []
    for port in ports:
        while threading.active_count() > max_threads:
            pass

        thread  = threading.Thread(target=port_scan, args=(tar,port))
        thread.start()
        threads.append(thread)
        


    for thread in threads:
        thread.join()


def service_detect (port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"



def grab_ban(socket_conn, timeout =1):
    try:
        socket_conn.settimeout(timeout)

        socket_conn.send(b"HELLO\r\n")
        return socket_conn.recv(1024).decode(errors="ignore").strip()
    
    except:
        return "No banner Grabbed"








print(f"\n Scanning {tar} (ports 1-{p}) ")

multi_threading(tar,ports,t)

print(f"The scan is completed")

if open_ports:
    print("OPEN PORTS FOUND:")
    for port,service in zip(sorted(open_ports),serv_dtc):
       
        print(f"→ Port {port} : {service} ")
else:
    print("No open ports found.")
print("-" * 30)


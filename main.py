import argparse
import socket
import threading

tar="steminfinity.in"#input("Enter the target: ")
p=200#int(input("Enter the port number: "))
t=30#int(input("Enter number of threads: "))
ports = range(1,p)

open_ports= []
serv_dtc = []


def port_scan(tar,port):
    try:
        
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((tar,port))

        if result == 0 :
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ser=service_detect(port)
            print(f"[+] Port {port} is open : {ser}", end='\r')
            open_ports.append(port)
            serv_dtc.append(ser)
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


print(f"\n Scanning {tar} (ports 1-{p}) ")

multi_threading(tar,ports,t)

print(f"The scan is completed")

if open_ports:
    print("OPEN PORTS FOUND:")
    for port,service in zip(sorted(open_ports)):
       
        print(f"→ Port {port} : {service} ")
else:
    print("No open ports found.")
print("-" * 30)


print(serv_dtc)
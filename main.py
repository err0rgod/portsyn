import argparse
import socket
import threading

tar=input("Enter the target: ")
p=int(input("Enter the port number: "))
t=int(input("Enter number of threads: "))
ports = range(1,p)




def port_scan(tar,port):
    try:
        
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((tar,port))

        if result == 0 :
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"the port {port} is Open")
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





print(f"\n Scanning {tar} (ports 1-{p}) ")

multi_threading(tar,ports,t)

print(f"The scan is completed")
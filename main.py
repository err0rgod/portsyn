import argparse
#for taking user input directly while interpretion
import socket
#for packet manipulation and connetion over a network
import threading
#for creating multiple threads
import socks
#for using socks5,4 to switch proxies 
from itertools import cycle
#looping over the list of proxies

tar="steminfinity.in"#input("Enter the target: ")
p=50#int(input("Enter the port number: "))
t=30#int(input("Enter number of threads: "))
ports = range(1,p)

open_ports= []    #storing the list of open ports to show up in the end
serv_dtc = []      #same with service detection 


USE_PROXY = True  # Toggle proxy on/off

proxy_ip = "185.59.100.55" #obiviously proxy ip
proxy_port = 1080


#proxy_pool = cycle(PROXY)


def port_scan(tar,port):          #main function for scanning ports and connecting other functions
    try:
        if USE_PROXY:               #for the switch to turn on/off proxy
            socks.set_default_proxy(socks.SOCKS5, proxy_ip, 1080) #setting up proxy ip and port
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
          #initializing the connection from the default proxy setted up in above line if switch is on the will connect to proxy otherwise will connet to system proxy
        s.settimeout(1)  

        result = s.connect_ex((tar,port))          #providing target and port to socket if alive will return 0 otherwise 1

        if result == 0 :           #if the target and port is alive then this statement will execute
 
            ser=service_detect(port)         #calling service detection func 
            banner = grab_ban(s)                #calling banner garabbing func

            print(f"[+] Port {port} is open : {ser}  :  {banner[:50]} : proxy :  {proxy_ip}", end='\r')         # providing user output


            open_ports.append(port)                
            serv_dtc.append((ser,banner))           #storing the port service and banners in a list mentioned above in the program
        else:
            print(f"port {port} not open. Failure. with proxy {proxy_ip}")
        s.close()
    
    except Exception as e:
        print(f"Error while scanning port {port} {e}")



def multi_threading(tar,ports,max_threads=10):          #for multi threading 
    threads = []
    for port in ports:
        while threading.active_count() > max_threads:
            pass

        thread  = threading.Thread(target=port_scan, args=(tar,port))
        thread.start()
        threads.append(thread)
        


    for thread in threads:
        thread.join()


def service_detect (port):            #for service detection using socket
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"



def grab_ban(socket_conn, timeout =1):            #basic banner grabbing function
    try:
        socket_conn.settimeout(timeout)

        socket_conn.send(b"HELLO\r\n")
        return socket_conn.recv(1024).decode(errors="ignore").strip()
    
    except:
        return "No banner Grabbed"


#end program code to be executed for providing smooth results to user

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


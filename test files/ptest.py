import argparse
import socket
import socks
import threading
from sys import exit

# Proxy Configuration (preserved from original)
PROXY_IP = "185.59.100.55"  
PROXY_PORT = 1080           
PROXY_USER = "username"     
PROXY_PASS = "password"     

# Shared lists (preserved from original)
open_ports = []
serv_dtc = []

# Argument Parser Setup
parser = argparse.ArgumentParser(description="Advanced port scanner by errorpad")
parser.add_argument("-t","--target", help="Target hostname or IP to scan")
parser.add_argument("-p", "--ports", type=str, default="1-200", help="Port range (e.g., 20-80)")
parser.add_argument("-c", "--threads", type=int, default=30, help="Number of threads")
parser.add_argument("--proxy", action="store_true", help="Enable proxy")

# Output format group (mutually exclusive)
output_group = parser.add_mutually_exclusive_group()
output_group.add_argument("-b", "--banner", action="store_true", help="Show brief banner info")
output_group.add_argument("-d", "--detailed", action="store_true", help="Show full banner output")

args = parser.parse_args()

# Port range parsing
try:
    start_port, end_port = map(int, args.ports.split('-'))
    ports = range(start_port, end_port + 1)
except ValueError:
    print("Error: Invalid port range format. Use START-END (e.g., 20-80)")
    exit(1)

def port_scan(tar, port):
    try:
        if args.proxy:
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, PROXY_IP, PROXY_PORT, 
                       username=PROXY_USER, password=PROXY_PASS)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        s.settimeout(1)
        result = s.connect_ex((tar, port))

        if result == 0:
            service = service_detect(port)
            banner = grab_banner(s) if (args.banner or args.detailed) else ""
            
            open_ports.append(port)
            serv_dtc.append((service, banner))
            
            if args.detailed:
                print(f"[+] Port {port} open : {service}")
            elif args.banner:
                print(f"[+] Port {port} open : {service}", end='\r')
        s.close()
    
    except Exception as e:
        if args.detailed:  # Only show errors in detailed mode
            print(f"Error while scanning port {port}: {e}")

def multi_threading(tar, ports, max_threads=10):
    threads = []
    for port in ports:
        while threading.active_count() > max_threads:
            pass

        thread = threading.Thread(target=port_scan, args=(tar, port))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def service_detect(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

def grab_banner(s):
    try:
        s.send(b"HELLO\r\n")
        return s.recv(1024).decode(errors="ignore").strip()
    except:
        return "No banner grabbed"

def show_results():
    if not open_ports:
        print("No open ports found.")
        return
        
    if args.detailed:
        print("\n" + "="*50)
        print(f"Detailed Scan Results for {args.target}")
        print("="*50)
        for port, (service, banner) in zip(open_ports, serv_dtc):
            print(f"\n[Port {port}] {service.upper()}")
            if banner and banner != "No banner grabbed":
                print("-"*40)
                print(banner)
                
    elif args.banner:
        print("\n" + "="*50)
        print(f"Brief Scan Results for {args.target}")
        print("="*50)
        for port, (service, banner) in zip(open_ports, serv_dtc):
            clean_banner = banner.split('\r\n')[0][:60] if banner else ""
            print(f"→ Port {port}: {service} | {clean_banner}")
    else:
        print("\nOpen ports:")
        for port, (service, _) in zip(open_ports, serv_dtc):
            print(f"→ Port {port}: {service}")

# Main execution
print(f"\n Scanning {args.target} (ports {args.ports}) with {args.threads} threads")
if args.proxy:
    print("Proxy: ENABLED")
multi_threading(args.target, ports, args.threads)
show_results()
print("\nScan completed!")
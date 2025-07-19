import argparse
import socket
import threading
import socks
import random
from sys import exit

# Argument Parser
parser = argparse.ArgumentParser(description="Advanced port scanner by err0rgod")
parser.add_argument("-t", "--target", type=str, required=True, help="Enter the target to scan the port")
parser.add_argument("-p", "--portse", type=str, default="1-1024", help="Enter the start and end of ports to scan")
parser.add_argument("-c", "--concurrency", type=int, default=10, help="Enter the number of threads")
parser.add_argument("-np", "--no_proxy", action="store_true", help="For not using proxy system")

# Output modes
output_group = parser.add_mutually_exclusive_group()
output_group.add_argument("-b", "--banner", action="store_true", help="Show brief banner info")
output_group.add_argument("-d", "--detailed", action="store_true", help="Show full banner output")

args = parser.parse_args()

# Global storage
open_ports = []    # Stores open ports
serv_dtc = []      # Stores service and banner data

# Proxy Configuration
PROXY_LIST = [
    "185.59.100.55:1080",
    "185.199.229.156:1080"  # Added secondary proxy
]

# Parse port range
try:
    start_port, end_port = map(int, args.portse.split('-'))
    ports = range(start_port, end_port + 1)
except ValueError:
    print("Error: Invalid port format. Use START-END (e.g., 1-100)")
    exit(1)

def get_random_proxy():
    """Selects a random proxy from PROXY_LIST"""
    proxy_str = random.choice(PROXY_LIST)
    parts = proxy_str.split(":")
    return {
        "host": parts[0],
        "port": int(parts[1])
    }

def service_detect(port):
    """Identifies service running on port"""
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

def grab_ban(sock):
    """Grabs banner from open port"""
    try:
        sock.send(b"HELLO\r\n")
        return sock.recv(1024).decode(errors="ignore").strip()
    except:
        return "No banner grabbed"

def port_scan(target, port):
    """Direct connection scan"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((target, port)) == 0:
                service = service_detect(port)
                banner = grab_ban(s) if (args.banner or args.detailed) else ""
                
                open_ports.append(port)
                serv_dtc.append((service, banner))
                
                if args.detailed:
                    print(f"[+] Port {port} open : {service}")
                elif args.banner:
                    print(f"[+] Port {port} open : {service}", end='\r')
    except Exception as e:
        if args.detailed:
            print(f"Error scanning port {port}: {e}")

def proxy_scan(target, port):
    """Proxy-rotating scan"""
    proxy = get_random_proxy()
    try:
        with socks.socksocket() as s:
            s.set_proxy(socks.SOCKS5, proxy["host"], proxy["port"])
            s.settimeout(2)
            if s.connect_ex((target, port)) == 0:
                service = service_detect(port)
                banner = grab_ban(s) if (args.banner or args.detailed) else ""
                
                open_ports.append(port)
                serv_dtc.append((service, banner))
                
                proxy_info = f"via {proxy['host']}" if not args.no_proxy else "direct"
                print(f"[+] Port {port} open : {service} : {banner[:50]} : {proxy_info}", end='\r')
    except Exception as e:
        if args.detailed:
            print(f"Proxy {proxy['host']} failed: {e}")

def scan(target, port):
    """Scan dispatcher"""
    if args.no_proxy:
        port_scan(target, port)
    else:
        proxy_scan(target, port)

def multi_threading(target, ports, max_threads):
    """Manages scanning threads"""
    threads = []
    for port in ports:
        while threading.active_count() > max_threads:
            pass
        thread = threading.Thread(target=scan, args=(target, port))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

def show_result():
    """Displays scan results"""
    if not open_ports:
        print("No open ports found")
        return
    
    if args.detailed:
        print("\n" + "="*50)
        print(f"Detailed Results for {args.target}")
        print("="*50)
        for port, (service, banner) in zip(open_ports, serv_dtc):
            print(f"\n[Port {port}] {service.upper()}")
            if banner != "No banner grabbed":
                print("-"*50)
                print(banner)
    
    elif args.banner:
        print("\n" + "="*50)
        print(f"Brief Results for {args.target}")
        print("="*50)
        for port, (service, banner) in zip(open_ports, serv_dtc):
            print(f"→ {port}: {service} | {banner.splitlines()[0][:60]}...")
    
    else:
        print("\nOpen ports:")
        for port, (service, _) in zip(open_ports, serv_dtc):
            print(f"→ {port}: {service}")

# Main execution
print(f"\nScanning {args.target} (ports {args.portse})")
multi_threading(args.target, ports, args.concurrency)
show_result()
print("\nScan completed!")
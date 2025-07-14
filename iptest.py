import socks
import socket

# Proxy setup
PROXY_IP = "185.59.100.55"
PROXY_PORT = 1080

# Apply SOCKS5 proxy globally
socks.set_default_proxy(socks.SOCKS5, PROXY_IP, PROXY_PORT)
socket.socket = socks.socksocket

# Test connection
try:
    s = socket.socket()
    s.settimeout(10)
    s.connect(("example.com", 80))
    s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    response = s.recv(4096)
    if b"Example Domain" in response:
        print("✓ Proxy working!")
    else:
        print("✗ Proxy connected but unexpected response")
    s.close()
except Exception as e:
    print(f"✗ Proxy failed: {e}")

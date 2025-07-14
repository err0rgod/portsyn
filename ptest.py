import socks
import socket

# Configure proxy (replace with your details)
PROXY_IP = "185.59.100.55"  # Proxy server IP
PROXY_PORT = 1080              # Default SOCKS5 port
#'''USERNAME = "your_username"     # Leave empty if no auth
#PASSWORD = "your_password"'''     # Leave empty if no auth

# Patch the socket
socks.set_default_proxy(
    socks.SOCKS5,
    PROXY_IP,
    PROXY_PORT,
    #username=USERNAME,
    #password=PASSWORD
)
socket.socket = socks.socksocket  # All sockets will now use this proxy

# Test connection
try:
    s = socket.socket()
    s.connect(("example.com", 80))
    print("✓ Proxy working!")
    s.close()
except Exception as e:
    print(f"✗ Proxy failed: {e}")

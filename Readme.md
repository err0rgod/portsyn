# Advanced Python Port Scanner

A multi-threaded, proxy-capable port scanner written in Python. Supports banner grabbing, service detection, and flexible output modes. Designed for fast and advanced scanning of network hosts.

## Features

- **Multi-threaded scanning** for speed
- **SOCKS5 proxy support** (with rotation)
- **Banner grabbing** for open ports
- **Service detection** using port numbers
- **Flexible output:** brief or detailed scan results
- **Customizable port ranges and concurrency**

## Usage

```sh
python main.py -t <target> [options]
```

### Options

- `-t, --target` **(required)**: Target hostname or IP to scan
- `-p, --portse`: Port range (default: `1-1024`, format: `start-end`)
- `-c, --concurrency`: Number of threads (default: `10`)
- `-np, --no_proxy`: Disable proxy usage
- `-b, --banner`: Show brief banner info
- `-d, --detailed`: Show full banner output

**Note:** `-b` and `-d` are mutually exclusive.

### Example

```sh
python main.py -t example.com -p 20-100 -c 30 -b
```

## Proxy Configuration

Edit the `PROXY_LIST` in [main.py](main.py) to add or change SOCKS5 proxies:

```python
PROXY_LIST = [
    "185.59.100.55:1080",
    "185.59.100.55:1080"
]
```

## Output

- **Brief mode:** Shows open ports with service and banner summary.
- **Detailed mode:** Shows open ports with full banner and service info.
- **Default:** Lists open ports and detected services.

## Requirements

- Python 3.x
- `PySocks` library (`pip install pysocks`)

## Legal Notice

**Use this tool only on networks and systems you own or have explicit permission to test. Unauthorized scanning is illegal and unethical.**

---

Inspired by [main.py](main.py) and related scripts in this
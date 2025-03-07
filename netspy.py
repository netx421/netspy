## netx421@proton.me 
import socket
import subprocess
import requests
import time
import os


# Cache to store IP lookups (avoid redundant requests)
ip_cache = {}

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Get active connections using ss
def get_active_connections():
    result = subprocess.run(["ss", "-tn"], capture_output=True, text=True).stdout
    lines = result.split("\n")[1:]  # Skip headers
    ips = set()
    
    for line in lines:
        parts = line.split()
        if len(parts) > 4:
            ip_port = parts[4]  # Destination IP:Port
            ip = ip_port.rsplit(":", 1)[0]  # Extract IP
            # Exclude localhost and private IPs (192.168.x.x, 10.x.x.x, 172.16-31.x.x)
            if not ip.startswith(("127.", "::1", "192.168.", "10.", "172.16", "172.17", "172.18", "172.19", "172.20", "172.21", "172.22", "172.23", "172.24", "172.25", "172.26", "172.27", "172.28", "172.29", "172.30", "172.31")):
                ips.add(ip)
    
    return ips

# Lookup hostname
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return ip  # Return IP if hostname is not found

# Lookup organization and location using ipinfo.io
def get_org_and_location(ip):
    if ip in ip_cache:
        return ip_cache[ip]  # Return cached result
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,org", timeout=2)
        data = response.json()
        org = data.get("org", "Unknown")
        location = f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}"
        ip_cache[ip] = (org, location)  # Store result in cache
        return org, location
    except requests.RequestException:
        return "Unknown", "Unknown"

# Main function to run in a loop
def main():
    while True:
                                            
        clear_screen()
        connections = get_active_connections()
        print("███╗   ██╗███████╗████████╗███████╗██████╗ ██╗   ██╗")
        print("████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗╚██╗ ██╔╝")
        print("██╔██╗ ██║█████╗     ██║   ███████╗██████╔╝ ╚████╔╝ ")
        print("██║╚██╗██║██╔══╝     ██║   ╚════██║██╔═══╝   ╚██╔╝  ")
        print("██║ ╚████║███████╗   ██║   ███████║██║        ██║   ")
        print("╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚═╝        ╚═╝   ")

        print(f"{'IP Address':<20} {'Host':<40} {'Organization':<30} {'Location':<20}")
        print("=" * 115)

        for ip in connections:
            host = get_hostname(ip)
            org, location = get_org_and_location(ip)
            print(f"{ip:<20} {host:<40} {org:<30} {location:<20}")
        print("=" * 115)
        print("netx421@proton.me")
        print(" ")
        print("Always Watching")
        time.sleep(15)

if __name__ == "__main__":
    main()

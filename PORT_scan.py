import time
from scapy.all import *

def scan_ports(ip_address, ports=None, delay=0.5):
    """
    Scans a list of ports on a given IP address to check if they are open, with a delay between each scan.

    Parameters:
    ip_address (str): The IP address to scan.
    ports (list, optional): A list of port numbers to scan. Defaults to all ports (0-65535) if None.
    delay (float): The delay in seconds between each port scan to avoid blocking. Default is 0.5 seconds.

    Returns:
    dict: A dictionary with port numbers as keys and their status ('open' or 'closed/filtered') as values.
    """
    if ports is None:
        ports = range(0, 65536)  # Scan all ports if no specific ports are provided
    
    port_status = {}

    for port in ports:
        # Crafting a TCP SYN packet
        syn_packet = IP(dst=ip_address)/TCP(dport=port, flags="S")
        
        # Sending the packet and waiting for a response
        response = sr1(syn_packet, timeout=1, verbose=False)
        
        # Checking the response to determine if the port is open
        if response:
            if response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
                port_status[port] = 'open'
                print(f"Port {port} is open")
            else:
                port_status[port] = 'closed/filtered'
                print(f"Port {port} is closed or filtered")
        else:
            port_status[port] = 'closed/filtered'
            print(f"Port {port} is closed or filtered")

        # Delay between each scan to avoid triggering security mechanisms
        time.sleep(delay)

    return port_status

# Example usage
if __name__ == "__main__":
    ip_address = "93.184.216.34"  # Example IP address (example.com)
    scan_results = scan_ports(ip_address, delay=0.5)
    print("Scan results:", scan_results)

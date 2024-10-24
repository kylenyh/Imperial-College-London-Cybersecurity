
# Import the os library for interacting with the operating system
import os
# Provides functions for interacting with the operating system, such as checking privileges and executing system commands

# Import the sys library for system-specific parameters and functions
import sys
# Offers functions and variables used to manipulate different parts of the Python runtime environment

# Import the time library for time-related functions
import time
# Supplies various time-related functions

# Import the defaultdict class from the collections library
from collections import defaultdict
# A dictionary subclass that calls a factory function to supply missing values

# Import the sniff function and IP, TCP, UDP, and ICMP classes from the scapy.all library
from scapy.all import sniff, IP, TCP, UDP, ICMP


# Define threshold for packet rate (packets per second)
THRESHOLD = 20
print(f"THRESHOLD: {THRESHOLD}")

# Packet callback function
def packet_callback(packet):
    """
    Process each packet, update packet count, and block IP if packet rate exceeds threshold.
    """
    
    # Check if packet has IP layer
    if packet.haslayer(IP):
        # Get source IP address from packet
        src_ip = packet[IP].src
        
        # Increment packet count for source IP
        packet_count[src_ip] += 1

        # Calculate time interval since last reset
        current_time = time.time()
        time_interval = current_time - start_time[0]
        
        # Reset packet count and update start time every second
        if time_interval >= 1:
            # Calculate packet rate for each IP
            for ip, count in packet_count.items():
                packet_rate = count / time_interval
                # Log packet rate for debugging purposes
                #print(f"IP: {ip}, Packet rate: {packet_rate}")  
                
                # Block IP if packet rate exceeds threshold and IP is not already blocked
                if packet_rate > THRESHOLD and ip not in blocked_ips:
                    print(f"Blocking IP: {ip}, packet rate: {packet_rate}")
                    # Add iptables rule to block IP
                    os.system(f"iptables -A INPUT -s {ip} -j DROP")
                    blocked_ips.add(ip)
            
            # Reset packet count and start time
            packet_count.clear()
            start_time[0] = current_time


# Function to restore iptables rules on exit
def restore_iptables():
    """
    Flush iptables rules to restore original configuration.
    """
    os.system("iptables -F")


if __name__ == "__main__":
    # Check for root privileges
    if os.getpid() != 0:
        print("This script requires root privileges.")
        sys.exit(1)

    # Initialize variables
    packet_count = defaultdict(int)
    start_time = [time.time()]
    blocked_ips = set()

    print("Monitoring network traffic...")
    
    # Register restore_iptables function to run on exit
    import atexit
    atexit.register(restore_iptables)
    
    # Start sniffing IP packets and call packet_callback for each packet
    sniff(filter="ip", prn=packet_callback)

# Basic firewall simulation system

import random  # Import the random module for generating random IP addresses and numbers


def generate_random_ip():
    """
    Generate a random IP address within the 192.168.1.x subnet.
    
    Returns:
        str: A random IP address in the format "192.168.1.x" where x is between 0 and 40.
    """
    # Generate a random number between 0 and 40 for the last octet of the IP address
    return f"192.168.1.{random.randint(0, 50)}"


def check_firewall_rules(ip, rules):
    """
    Check if the IP address matches any firewall rule and return the corresponding action.
    
    Args:
        ip (str): The IP address to check.
        rules (dict): A dictionary of firewall rules where keys are IP addresses and values are actions.
    
    Returns:
        str: The action to take for the given IP address ("block" or "allow").
    """
    # Iterate through each rule in the firewall rules dictionary
    for rule_ip, action in rules.items():
        # Check if the IP address matches the current rule
        if ip == rule_ip:
            # If it matches, return the corresponding action
            return action
    # If no rule matches, return the default action ("allow")
    return "allow"


def main():
    """
    Simulate network traffic by generating random IP addresses and checking them against firewall rules.
    """
    # Define the firewall rules (key: IP address, value: action)
    firewall_rules = {
        "192.168.1.1": "block",
        "192.168.1.4": "block",
        "192.168.1.9": "block",
        "192.168.1.13": "block",
        "192.168.1.16": "block",
        "192.168.1.19": "block"
    }
    
    # Simulate network traffic by generating 12 random IP addresses
    for _ in range(20):
        # Generate a random IP address
        ip_address = generate_random_ip()
        
        # Check the IP address against the firewall rules
        action = check_firewall_rules(ip_address, firewall_rules)
        
        # Generate a random number for demonstration purposes
        random_number = random.randint(0, 10000)
        
        # Print the IP address, action, and random number
        print(f"IP: {ip_address}, Action: {action}, Random: {random_number}")


# Ensure the main function is executed when the script is run directly
if __name__ == "__main__":
    main()

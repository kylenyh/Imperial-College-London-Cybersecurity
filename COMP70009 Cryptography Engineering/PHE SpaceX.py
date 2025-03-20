
# Scenario
# SpaceX is working on a project to optimize fuel consumption for its rockets during various phases of a mission. 
# The company wants to securely store and process sensitive data related to fuel usage without revealing the actual values to unauthorized personnel. 
# They decide to use homomorphic encryption to allow computations on encrypted data. 
# For example, they need to calculate the total fuel consumption for a mission, determine the difference in fuel usage between two stages of the flight, apply a fixed percentage increase to the fuel efficiency, and divide the fuel consumption by a certain factor for analysis.

# Homomorphic encryption (HE) allows computations on encrypted data without decrypting it. There are three main types:

# Partially Homomorphic Encryption (PHE)
# Supports only one operation (addition or multiplication) an unlimited number of times.

# Somewhat Homomorphic Encryption (SHE)
# Supports both addition and multiplication but only a limited number of times before noise corrupts the ciphertext.

# Fully Homomorphic Encryption (FHE)
# Supports both addition and multiplication an unlimited number of times, enabling complex computations on encrypted data.

# A Python 3 library implementing the Paillier Partially Homomorphic Encryption.

from phe import paillier
import random

def main():
    # Step 1: Key Generation (Public & Private Keys)
    public_key, private_key = paillier.generate_paillier_keypair()

    # Step 2: Encrypt Fuel Consumption Data for Two Stages
    stage1_fuel = 5000  # Fuel consumption for stage 1 in liters
    stage2_fuel = 3000  # Fuel consumption for stage 2 in liters

    cipher_stage1_fuel = public_key.encrypt(stage1_fuel)
    cipher_stage2_fuel = public_key.encrypt(stage2_fuel)

    print(f"Encrypted Stage 1 Fuel: {cipher_stage1_fuel}")
    print(f"Encrypted Stage 2 Fuel: {cipher_stage2_fuel}")

    # Step 3: User Menu for Operation Choice
    print("Choose an operation:")
    print("1. Calculate Total Fuel Consumption")
    print("2. Determine Difference in Fuel Usage Between Two Stages")
    print("3. Apply Fixed Percentage Increase to Fuel Efficiency")
    print("4. Divide Fuel Consumption by a Certain Factor")

    choice = input("Enter the number of your choice: ")

    if choice == '1':
        # Calculate Total Fuel Consumption
        cipher_total_fuel = cipher_stage1_fuel + cipher_stage2_fuel
        decrypted_total_fuel = private_key.decrypt(cipher_total_fuel)
        print(f"Decrypted Total Fuel Consumption: {decrypted_total_fuel} liters")  # Should print 8000 liters

    elif choice == '2':
        # Determine Difference in Fuel Usage Between Two Stages
        cipher_diff_fuel = cipher_stage1_fuel - cipher_stage2_fuel
        decrypted_diff_fuel = private_key.decrypt(cipher_diff_fuel)
        print(f"Decrypted Difference in Fuel Usage: {decrypted_diff_fuel} liters")  # Should print 2000 liters

    elif choice == '3':
        # Apply Fixed Percentage Increase to Fuel Efficiency
        efficiency_increase_percentage = 0.10  # 10% increase
        cipher_efficiency_increase = cipher_stage1_fuel * efficiency_increase_percentage
        decrypted_efficiency_increase = private_key.decrypt(cipher_efficiency_increase)
        print(f"Decrypted Efficiency Increase: {decrypted_efficiency_increase} liters")  # Should print 500 liters

    elif choice == '4':
        # Divide Fuel Consumption by a Certain Factor
        division_factor = 5
        try:
            cipher_div_fuel = cipher_stage1_fuel / division_factor
            decrypted_div_fuel = private_key.decrypt(cipher_div_fuel)
            print(f"Decrypted Division Result: {decrypted_div_fuel} liters")  # Should print 1000 liters
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed.")

    else:
        print("Invalid choice. Please restart the program and choose a valid option.")

if __name__ == "__main__":
    main()

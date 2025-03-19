

# Scenario: MFA in a Smart Healthcare System

# Background:
# A large hospital has implemented a smart healthcare system that allows doctors, nurses, and staff to access patient records, medical prescriptions, 
# and IoT-connected medical devices (like heart monitors and infusion pumps) remotely via a secure portal.

# Problem:
# Recently, there have been multiple attempts to access patient records from unauthorized devices. 
# Cybercriminals are trying to exploit weak passwords to steal medical data or tamper with connected medical devices. 
# The hospital's legal compliance (HIPAA, GDPR) requires strong authentication.




# Step 1: Load the libraries
import time # For time
import pyotp  # For generating TOTP (Time-based One-Time Password)
import hashlib  # For secure hashing of passwords




# Step 2: Define a predefined password
password = "SecureP@ss123"  # This is the password you will input

# Precompute the SHA-256 hash of the password for comparison
expected_password_hash = hashlib.sha256(password.encode()).hexdigest()




# Step 3: Ask for user input (password)
input_password = input("Enter your password: ")




# Step 4: Hash the entered password
input_password_hash = hashlib.sha256(input_password.encode()).hexdigest()





# Step 5: Validate the password
if input_password_hash == expected_password_hash:
    print("\nPassword is correct. Proceeding with 2FA...\n")
    
    
    
    

    # Step 6: Initialize 2FA (Time-based One-Time Password)
    totp = pyotp.TOTP(pyotp.random_base32())
    print(f"Your secret key (for first-time setup): {totp.secret}")

    time.sleep(10)  # Wait for 10 seconds before user enters the code
    



    # Step 7: Generate a 6-digit OTP code using the secret key and print it for testing
    otp_code = totp.now()  # Generate a 6-digit code
    print(f"Generated OTP Code: {otp_code}")  # You can remove this line after testing




    # Step 8: Ask for the OTP input
    input_code = input("Enter the 2FA Code: ")
    




    # Step 9: Validate the OTP code
    if totp.verify(input_code):
        print("2FA code is valid. Access granted.")
    else:
        print("Invalid 2FA code. Access denied.")
else:
    print("Incorrect password. Access denied.")






# Step 10: Log the login attempt (successful or failed)
def log_attempt(success):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    status = "SUCCESS" if success else "FAILED"
    with open("login_attempts.log", "a") as log_file:
        log_file.write(f"{timestamp} - Login attempt {status}\n")

# After verification:
if totp.verify(input_code):
    print("2FA code is valid. Access granted.")
    log_attempt(True)  # Log successful attempt
else:
    print("Invalid 2FA code. Access denied.")
    log_attempt(False)  # Log failed attempt




# Scenario
# A financial institution wants to establish a highly secure communication channel between its headquarters in London and its data center in New York.
# To prevent any potential cyber threats or eavesdropping, they decide to use the BB84 Quantum Key Distribution (QKD) protocol over a fiber-optic network.


# Quantum Key Distribution (QKD) is a secure way to share encryption keys using quantum mechanics. 
# It ensures that any attempt to eavesdrop on the key will be detected, making the communication highly secure. 
# The most common method, BB84, uses photons (light particles) to transmit key bits, which change if intercepted, alerting the users.


# Alice is the sender and Bob is the receiver





# Step 1: Load the libraries 
import numpy as np  # For generating random numbers and handling numerical operations
from qiskit import QuantumCircuit, Aer, execute  # For creating and simulating quantum circuits
import hashlib  # For generating hash values (used in key verification and authentication)
from Crypto.Cipher import AES  # For AES encryption and decryption
from Crypto.Util.Padding import pad, unpad  # For adding/removing padding in AES encryption
import os  # For generating random initialization vectors (IV) and handling file operations





# Step 2: Generate random bits and bases

# Number of qubits 
num_qubits = 1024 # Larger number for larger simulations
print("Number of qubits: ", num_qubits) # prints number of qubits 

# Alice's bits (random choice)
alice_bits = np.random.randint(2, size = num_qubits) # Alice's random bits
print("Alice's bits: ", alice_bits) # Prints Alice's random bits

# Alice's bases (random choice)
alice_bases = np.random.randint(2, size = num_qubits) # 0: Standard basis, 1: Hadamard basis
print("Alice's bases: ", alice_bases) # Prints Alice's random bases

# Bob's bases (random choice)
bob_bases = np.random.randint(2, size = num_qubits) # Bob's random measurement bases
print("Bob's bases: ", bob_bases) # Prints Bob's random bases

# Bob's results
bob_results = [] # Bob's results stored in a list
print("Bob's results: ", bob_results) # Prints Bob's results

# Quantum simulator backend
backend = Aer.get_backend('qasm_simulator')

for i in range(num_qubits):
    qc = QuantumCircuit(1, 1)

    # Encode Alice's qubits
    if alice_bits[i] == 1:
        qc.x(0)  # Apply X gate for bit 1

    if alice_bases[i] == 1:
        qc.h(0)  # Hadamard basis encoding

    # Bob's measurement
    if bob_bases[i] == 1:
        qc.h(0)  # If Bob chose Hadamard, apply H before measurement

    qc.measure(0, 0)

    # Simulate measurement
    result = execute(qc, backend, shots = 1).result() # Executes process 
    print("Result: ", result) # Prints the result 

    measured_bit = int(list(result.get_counts().keys())[0]) # Gets the measured bit
    print("Result: ", result) # Prints the result 

    bob_results.append(measured_bit) # Adds measured bit to Bob's results
    print("Bob's results: ", bob_results) # Prints Bob's results






# Step 3: Sifting Phase (Keep bits where bases match)
shared_key = [alice_bits[i] for i in range(num_qubits) if alice_bases[i] == bob_bases[i]] # Gets shared key following the conditional statement
print("Shared key: ", shared_key) # Prints shared key





# Step 4: Simulate eavesdropping attack (Eve)
eve_bases = np.random.randint(2, size = num_qubits) # Eve chooses random bases
print("Eve's bases: ", eve_bases) # Prints Eve's random bases

eve_results = [] # Eve's results stored in a list
print("Eve's results: ", eve_results) # Prints Eve's results

for i in range(num_qubits):
    qc = QuantumCircuit(1, 1)

    # Encode Alice's qubits
    if alice_bits[i] == 1:
        qc.x(0)  

    if alice_bases[i] == 1:
        qc.h(0)

    # Eve intercepts and measures
    if eve_bases[i] == 1:
        qc.h(0)  

    qc.measure(0, 0)
    result = execute(qc, backend, shots = 1).result() # Gets new result for Eve
    print("Result: ", result) # Prints the result

    eve_results.append(int(list(result.get_counts().keys())[0])) # Adds new results to Eve's results
    print("Eve's results: ", eve_results) # Prints Eve's results

    # Eve resends the qubit to Bob
    qc = QuantumCircuit(1, 1)
    if eve_results[i] == 1:
        qc.x(0)  
    if eve_bases[i] == 1:
        qc.h(0)

    # Bob's measurement
    if bob_bases[i] == 1:
        qc.h(0)  

    qc.measure(0, 0)
    result = execute(qc, backend, shots = 1).result() # Gets new result for Bob
    bob_results[i] = int(list(result.get_counts().keys())[0]) # Overwrite Bob's results





# Step 5: Classic authentication step

shared_key_str = ''.join(map(str, shared_key)) # Gets the shared key (str)
print("Shared key (str): ", shared_key_str) # Prints the shared key (str)

key_hash = hashlib.sha256(shared_key_str.encode()).hexdigest() # Gets the hashed key
print("Hashed shared key: ", key_hash) # Prints the hashed key





# Step 6: Error detection (Comparing Alice and Bob's bits)
errors = sum(1 for i in range(num_qubits) if alice_bases[i] == bob_bases[i] and alice_bits[i] != bob_results[i])

error_rate = errors / max(1, len(shared_key)) * 100 # Avoid division by zero
print(f"Error Rate: {error_rate: .2f}%") # Prints error rate

if error_rate > 10: # Conditional statement for error rate
    print("Warning! Possible eavesdropping detected. Abort communication.")
else:
    print("Key exchange successful. No significant eavesdropping detected.")




# Step 7: Shared key conversion

# Convert shared key to 16-byte AES key
aes_key = hashlib.sha256(shared_key_str.encode()).digest()[:16] # The AES key
print("AES key: ", aes_key) # Prints the AES key

# Encrypt a sample message
cipher = AES.new(aes_key, AES.MODE_CBC, iv = os.urandom(16)) # The cipher
print("Cipher: ", cipher) # Prints the cipher

message = "Secure communication between London and New York" # The message
print("Message: ", message) # Prints the message

ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
print("Encrypted Message:", ciphertext.hex()) # Prints the cipher text

# To decrypt:
cipher = AES.new(aes_key, AES.MODE_CBC, iv = cipher.iv) # The cipher
print("Cipher: ", cipher) # Prints the cipher

decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size).decode() # Decrypted message
print("Decrypted Message:", decrypted_message) # Prints the decrypted message

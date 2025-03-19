
# Scenario: Secure Secret Santa Assignment for a Remote Team

# Background: A remote team of colleagues wants to organize a Secret Santa gift exchange for the holiday season. 
# Since they are spread across different locations, they need a secure way to assign Secret Santa pairs without revealing the assignments to anyone except the organizer. 
# They also want to ensure that no one is assigned themselves.

# MPyC is a Python package for secure multiparty computation (MPC)

# Import the libraries
import mpyc
import random
from mpyc.runtime import mpc

# Start the MPC runtime
mpc.run(mpc.start())

# List of participants
participants = []
num_participants = int(input("Enter the number of participants: "))
for _ in range(num_participants):
    participant = input("Enter participant name: ")
    participants.append(participant)

# Generate a secure random permutation of indices
indices = list(range(len(participants)))
random.shuffle(indices)

# Convert indices to secure integers
secint = mpc.SecInt(32)  # Secure 32-bit integers
secure_assignments = [secint(indices[i]) for i in range(len(participants))]


# Define an asynchronous function for secure Secret Santa assignment
# async =  defines an asynchronous function that can perform tasks concurrently, making it more efficient, especially when dealing with operations that involve waiting
async def secure_secret_santa():
    # Reveal the Secret Santa assignment securely
    revealed_assignments = await mpc.output(secure_assignments)

    # Ensure no one is assigned themselves
    while any(i == revealed_assignments[i] for i in range(len(participants))):
        random.shuffle(indices)
        new_secure_assignments = [secint(indices[i]) for i in range(len(participants))]
        revealed_assignments = await mpc.output(new_secure_assignments)

    # Display assignments
    for i in range(len(participants)):
        print(f"{participants[i]} is Secret Santa for {participants[revealed_assignments[i]]}")

# Run the secure Secret Santa function and shut down the MPyC runtime
mpc.run(secure_secret_santa())
mpc.run(mpc.shutdown())

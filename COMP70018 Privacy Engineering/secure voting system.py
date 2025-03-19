# Scenario: Secure Voting for a Student Council Election

# Background: A school is conducting a student council election with three candidates: Alice (A), Bob (B), and Charlie (C). 
# Five students are voting for their preferred candidate. 
# The school wants to ensure that the voting process is secure and private, so they decide to use Secure Multi-Party Computation (SMPC) to count the votes without revealing individual selections.

# MPyC is a Python package for secure multiparty computation (MPC)

# Import the library
import mpyc
from mpyc.runtime import mpc

# Starting the MPyC runtime
mpc.run(mpc.start())

# Secure integer type
secint = mpc.SecInt(32)

# async =  defines an asynchronous function that can perform tasks concurrently, making it more efficient, especially when dealing with operations that involve waiting
async def secure_multi_choice_voting():
    # Example: 3 candidates (A, B, C) and 5 voters choosing their candidate
    # Each vote is represented as an index (0 = A, 1 = B, 2 = C)
    votes = [0, 2, 1, 0, 2]  # Voter selections

    # Convert votes to one-hot encoded secure vectors
    num_candidates = 3
    secure_votes = [[secint(1 if v == c else 0) for c in range(num_candidates)] for v in votes]

    # Securely sum votes for each candidate
    total_votes = [mpc.sum([secure_votes[v][c] for v in range(len(votes))]) for c in range(num_candidates)]

    # Reveal only the final vote count for each candidate
    # await = pauses the execution of an async function until the result of an awaited coroutine or task is available
    final_tally = await mpc.output(total_votes)

    print("\nSecure Voting Results:")
    # enumrate = gets both the index and the value of each item in the iterable
    for i, count in enumerate(final_tally):
        print(f"Candidate {chr(65+i)}: {count} votes")

# Running the secure voting function and shutting down the MPyC runtime
mpc.run(secure_multi_choice_voting())
mpc.run(mpc.shutdown())

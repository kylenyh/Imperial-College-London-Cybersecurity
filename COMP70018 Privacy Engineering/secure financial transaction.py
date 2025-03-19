# Scenario: Secure Financial Transactions for a Joint Venture

# Background: Two companies, Company A and Company B, are collaborating on a joint venture. 
#They need to contribute funds to a shared project while ensuring that their individual contributions and remaining balances remain private. 
# They also want to log each transaction securely for auditing purposes.


# MPyC is a Python package for secure multiparty computation (MPC)

# Import the library
import mpyc
from mpyc.runtime import mpc

# Starting the MPyC runtime
mpc.run(mpc.start())

# Secure integer type
secint = mpc.SecInt(32)

# Define an asynchronous function for financial transaction system
# async =  defines an asynchronous function that can perform tasks concurrently, making it more efficient, especially when dealing with operations that involve waiting
async def secure_transaction():
    # Example: Two parties making transactions
    balances = [1000, 1500]  # Initial balances
    transaction_amounts = [500, 1000]  # Transaction amounts in dollars

    # Convert balances and transaction amounts to secure integers
    secure_balances = [secint(balance) for balance in balances]
    secure_amounts = [secint(amount) for amount in transaction_amounts]

    # Verify that each party has sufficient balance
    sufficient_balance = [mpc.ge(secure_balances[i], secure_amounts[i]) for i in range(len(transaction_amounts))]
    verified = await mpc.output(mpc.all(sufficient_balance))

    if verified:
        # Securely sum the transaction amounts
        total_amount = mpc.sum(secure_amounts)

        # Reveal the total transaction amount
        final_amount = await mpc.output(total_amount)
        print(f"Total Transaction Amount: ${final_amount}")

        # Update balances
        updated_balances = [mpc.sub(secure_balances[i], secure_amounts[i]) for i in range(len(transaction_amounts))]
        final_balances = await mpc.output(updated_balances)
        print(f"Updated Balances: {final_balances}")
    else:
        print("Insufficient balance for one or more parties.")

# Running the secure voting function and shutting down the MPyC runtime
mpc.run(secure_transaction())
mpc.run(mpc.shutdown())


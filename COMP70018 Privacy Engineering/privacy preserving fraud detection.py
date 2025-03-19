


# Scenario: Privacy-Preserving Fraud Detection for Financial Institutions

# Background: Financial institutions, such as banks, need to detect fraudulent activities while ensuring the privacy of their customers' data.
# Traditional methods of fraud detection often require sharing sensitive information, which can lead to privacy concerns.
# To address this, banks can use Secure Multi-Party Computation (SMPC) to collaboratively detect fraud without revealing individual transaction details.

# MPyC is a Python package for secure multiparty computation (MPC)

# Import the library
import mpyc
from mpyc.runtime import mpc

# Starting the MPyC runtime
mpc.run(mpc.start())

# Secure integer type
secint = mpc.SecInt(32)

# Define an asynchronous function for privacy-preserving fraud detection
async def secure_fraud_detection():
    # Example: Transaction amounts and risk scores from two banks
    transactions_bank1 = [100, 200, 300]  # Transaction amounts in dollars
    transactions_bank2 = [150, 250, 350]  # Transaction amounts in dollars
    risk_scores_bank1 = [1, 2, 3]  # Risk scores for transactions
    risk_scores_bank2 = [2, 3, 4]  # Risk scores for transactions

    # Convert transaction amounts and risk scores to secure integers
    secure_transactions_bank1 = [secint(amount) for amount in transactions_bank1]
    secure_transactions_bank2 = [secint(amount) for amount in transactions_bank2]
    secure_risk_scores_bank1 = [secint(score) for score in risk_scores_bank1]
    secure_risk_scores_bank2 = [secint(score) for score in risk_scores_bank2]

    # Securely sum the risk scores for each transaction
    total_risk_scores = [mpc.sum([secure_risk_scores_bank1[i], secure_risk_scores_bank2[i]]) for i in range(len(secure_risk_scores_bank1))]

    # Reveal only the final risk scores
    final_risk_scores = await mpc.output(total_risk_scores)

    print("\nSecure Fraud Detection Results:")
    for i, score in enumerate(final_risk_scores):
        print(f"Transaction {i+1}: Risk Score = {score}")

# Running the secure fraud detection function and shutting down the MPyC runtime
mpc.run(secure_fraud_detection())
mpc.run(mpc.shutdown())

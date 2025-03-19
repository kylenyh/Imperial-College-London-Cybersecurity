

# Scenario: A Simple Digital Payment Ledger for a Small Community
# Background:
# A local community has created a small-scale digital currency called "Neighborhood Coins (NC)" to facilitate transactions between residents without relying on traditional banks.
# They ask for q blockchain implementation that can serve as a basic transaction ledger to track how NC is sent between people securely.








# Step 1: Load the libraries
import hashlib  # For hashing the blocks
import rsa  # For digital signatures (install with `pip install rsa`)







# Step 2: Define the Block class
class Block:
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list
        self.nonce = 0
        self.block_data = "-".join(transaction_list) + "-" + previous_block_hash
        self.block_hash = self.calculate_hash()

    def calculate_hash(self):
        # Generates the SHA-256 hash of the block data.
        return hashlib.sha256((self.block_data + str(self.nonce)).encode()).hexdigest()

    def mine_block(self, difficulty):
        # Proof of Work: Finds a valid hash with leading zeros based on difficulty.
        target = "0" * difficulty  # Hash must start with `difficulty` number of 0s
        while self.block_hash[:difficulty] != target:
            self.nonce += 1
            self.block_hash = self.calculate_hash()
        print(f"Block mined: {self.block_hash}")






# Step 3: Define the Blockchain class
class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = difficulty  # Adjust mining difficulty

    def create_genesis_block(self):
        # Creates the first block with a default 'Genesis Block'
        return Block("0", ["Genesis Block"])

    def add_transaction(self, transaction):
        # Adds a transaction to the pending transaction pool
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        # Mines a new block containing pending transactions and adds it to the chain
        if not self.pending_transactions:
            print("No transactions to mine.")
            return
        
        new_block = Block(self.chain[-1].block_hash, self.pending_transactions)
        new_block.mine_block(self.difficulty) # Perform proof-of-work mining
        self.chain.append(new_block)
        self.pending_transactions = [] # Clear transactions after mining

    def is_valid_chain(self):
        # Checks the blockchain's integrity
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.block_hash != hashlib.sha256((current_block.block_data + str(current_block.nonce)).encode()).hexdigest():
                return False # Block data has been tampered with

            if current_block.previous_block_hash != previous_block.block_hash:
                return False # Chain is broken

        return True







# Step 4: Implement digital signatures
def generate_keys():
    # Generates a public-private key pair
    return rsa.newkeys(512)

def sign_transaction(private_key, transaction):
    # Digitally signs a transaction using a private key
    return rsa.sign(transaction.encode(), private_key, 'SHA-256')

def verify_transaction(public_key, transaction, signature):
    # Verifies if a transaction's signature is valid
    try:
        rsa.verify(transaction.encode(), signature, public_key)
        return True
    except:
        return False








# Step 5: Testing the Blockchain Implementation

# Generate keys for users
(public_key_A, private_key_A) = generate_keys()
(public_key_B, private_key_B) = generate_keys()

# Create a blockchain instance
my_blockchain = Blockchain()

# Create and sign transactions
t1 = "Anna sends 2 NC to Mike"
signature_t1 = sign_transaction(private_key_A, t1)
print(f"Transaction Verified? {verify_transaction(public_key_A, t1, signature_t1)}")

t2 = "Bob sends 4 NC to Mike"
signature_t2 = sign_transaction(private_key_B, t2)
print(f"Transaction Verified? {verify_transaction(public_key_B, t2, signature_t2)}")

# Add transactions to the blockchain
my_blockchain.add_transaction(t1)
my_blockchain.add_transaction(t2)

# Mine a new block
print("\nMining transactions...")
my_blockchain.mine_pending_transactions()

# Add another transaction
t3 = "Harry sends 10 NC to Charlie"
my_blockchain.add_transaction(t3)

# Mine another block
print("\nMining new transactions...")
my_blockchain.mine_pending_transactions()

# Print blockchain details
print("\nBlockchain:")
for i, block in enumerate(my_blockchain.chain):
    print(f"Block {i}:")
    print(f"Transactions: {block.transaction_list}")
    print(f"Block Hash: {block.block_hash}")
    print(f"Previous Hash: {block.previous_block_hash}")
    print("------")

# Validate the blockchain
print("\nIs blockchain valid?", my_blockchain.is_valid_chain())

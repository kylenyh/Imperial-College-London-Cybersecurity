
# Scenario
# A company wants to compute the total payroll securely without revealing individual employee salaries. 
# Employees' salaries are encrypted before sending them to the financial system, which computes the total payroll homomorphically.


# Homomorphic encryption (HE) allows computations on encrypted data without decrypting it. There are three main types:

# Partially Homomorphic Encryption (PHE)
# Supports only one operation (addition or multiplication) an unlimited number of times.

# Somewhat Homomorphic Encryption (SHE)
# Supports both addition and multiplication but only a limited number of times before noise corrupts the ciphertext.

# Fully Homomorphic Encryption (FHE)
# Supports both addition and multiplication an unlimited number of times, enabling complex computations on encrypted data.


# TenSEAL CKKS implementation falls under FHE because it allows encrypted arithmetic on floating-point numbers




# Step 1: Loads the libraries
import tenseal as ts # For HE system
import matplotlib.pyplot as plt # For plotting graph 
import numpy as np # For random number generator 




# Step 2: Creates a context for encryption
context = ts.context(
    scheme = ts.SCHEME_TYPE.CKKS, # Using CKKS scheme for floating-point operations
    poly_modulus_degree = 8192, # Defines the security level
    coeff_mod_bit_sizes = [60, 40, 40, 60]  # Encryption parameters
)

# Enables necessary functionalities
context.global_scale = 2**40  # Scaling factor for precision
context.generate_galois_keys()  # Enables rotation operations
context.generate_relin_keys()   # Enables multiplication operations




# Step 3: Encrypts employee salaries and other important data

# Employees salaries
salaries = [60000, 55000, 70000, 80000, 90000, 120000, 350000, 100000, 200000, 85000]  # Employee salaries
print("Salaries: ", salaries) # Prints the salaries

# Employees bonuses
bonuses = [4000, 3000, 7000, 5000, 10000, 80000, 2000, 6000, 7500, 9000]  # Performance bonuses
print("Bonuses: ", bonuses) # Prints the bonus

# Tax rate
tax_rate = 0.40  # 40% tax
print("Tax rate: ", tax_rate) # Prints the tax rate

# Employees deductions (healthcare, insurance, pension)
deductions = [3000, 4000, 2000, 1000, 3000, 5000, 7000, 6000, 8000, 2500]  # Healthcare, insurance, pension
print("Deductions: ", deductions) # Prints the deductions

# Encrypt the salary, bonus, deductions

# Encrypted employees salaries
enc_salaries = ts.ckks_vector(context, salaries) # Encrypted salary
print("Encrypted salaries: ", enc_salaries) # Prints the encrypted salaries

# Encrypted employees bonuses
enc_bonuses = ts.ckks_vector(context, bonuses) # Encrypted bonuses
print("Encrypted bonuses: ", enc_bonuses) # Prints the encrypted bonuses

# Encrypted employees deductions (healthcare, insurance, pension)
enc_deductions = ts.ckks_vector(context, deductions) # Encrypted deductions
print("Encrypted deductions: ", enc_deductions) # Prints the encrypted deductions




# Step 4: Performs secure payroll computation (aggregate employees' salaries)

# Net encrypted gross salary 
enc_net_gross_salary = enc_salaries + enc_bonuses  # Computes net gross salary
print("Encrypted net employee gross salary: ", enc_net_gross_salary) # Prints the encrypted salaries

# Net encrypted tax
enc_net_tax = enc_net_gross_salary * tax_rate  # Computes net tax
print("Encrypted net tax: ", enc_net_tax) # Prints the encrypted salaries

# Net encrypted salary
enc_net_salary = enc_net_gross_salary - enc_net_tax - enc_deductions  # Computes net salary
print("Encrypted net employee salary: ", enc_net_salary) # Prints the encrypted net salaries




# Step 5: Decrypts and retrieves the result

# Net decrypted salary
dec_net_salary = enc_net_salary.decrypt() # Decrypts net employee salary
print("Decrypted net employee salary: ", dec_net_salary) # Prints the decrypted net employee salaries




# Step 6: Graph plot

# Converts decrypted salaries to numpy array for plotting
dec_net_salary_graph = np.arange(len(dec_net_salary))  # Employee indices

# Plot the decrypted net salaries
plt.figure(figsize=(10, 5))
plt.bar(dec_net_salary_graph, dec_net_salary, color="green")

# Labels and title
plt.xlabel("Employee Index")
plt.ylabel("Net Salary ($)")
plt.title("Decrypted Net Salary per Employee")
plt.xticks(dec_net_salary_graph)  # Set employee indices as x-axis labels
plt.grid(axis = "y", linestyle = "--", alpha = 0.7)

# Show the plot
plt.show()

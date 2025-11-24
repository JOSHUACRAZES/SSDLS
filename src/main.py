import os

# ❌ VULNERABLE: user input is executed as a system command
filename = input("Enter a file name to view: ")
os.system(f"cat {filename}")

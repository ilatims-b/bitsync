##########################################################################################################################################################################3
"""
Name of the developer: Nithin

Date of development: 2/4/2025

Project: Finding the output of a given input through the channel matrix

Method used: Repititve Algorithm

Comments: Nice project, I enjoyed the challenge.


"""

import sys
import random

x = str(input("Enter the string: with only (a-z) and with ., :"))
x = x.lower()  # Convert input to lowercase to standardize

def check(x):
    # Function to validate if the string contains only allowed characters
    for i in range(len(x)):
        if x[i] not in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.',',',' ']:
            return False
    return True

if check(x):
    print("Valid string")
else:
    print("Invalid string")
    sys.exit()  # Exit program if input contains invalid characters

def get_key_from_value(char_mapping, value):
    # Function to retrieve the key from a dictionary given a value
    for key, val in char_mapping.items():
        if val == value:
            return key  # Returns the first match found
    return None  # Return None if value is not found

m_old = []  # List to store numerical representation of input string
char_mapping = {}  # Dictionary to store character-to-number mapping
num = 1  # Start number for mapping

# Mapping letters a-z with specific number pattern
for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz", start=1):
    if i % 3 == 1:
        char_mapping[ch] = num
    elif i % 3 == 2:
        char_mapping[ch] = num + 2
    else:
        char_mapping[ch] = num + 1
        num += 3  # Increment for the next set of characters

# Mapping special characters
char_mapping[','] = num + 1  # Assign ',' a unique number
char_mapping['.'] = num + 3
char_mapping[' '] = num + 4

# Convert input string to numerical representation using mapping
for i in range(len(x)):
    m_old.append(char_mapping[x[i]])
print(m_old)  # Print numerical representation

# Channel matrix defining transition probabilities
matrix= [[0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.3],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.3, 0.7]
 ]

m_final_listcheck = []  # Stores results of multiple iterations
for w in range(100):  # Repeating for error correction
    m_new = []  # Store modified values
    count = 0  # Counter for tracking position
    for i in m_old:
        r = random.random()  # Generate a random probability value
        l = 0  # Cumulative probability tracker
        k = 0  # Current probability range upper bound
        k = matrix[i-1][((i-1)//3)*3]  # Retrieve probability from matrix
        for j in range(((i-1)//3)*3, 29):  # Iterate through matrix row
            if len(m_new) != (count + 1):  # Ensure correct indexing
                if k > r >= l:  # Check probability bounds
                    if i not in [28,29]:  # Handle special cases for punctuation
                        if (j+1) % 3 == 0:
                            j = j -1  # Adjust index
                        elif (j+1) % 3 == 2:
                            j = j + 1  # Adjust index
                        m_new.append(j+1)  # Store mapped value
                        break
                    else:
                        m_new.append(j+1)  # Directly append for special cases
                else:
                    l = matrix[i-1][j] + l  # Update lower probability bound
                    k = matrix[i-1][j+1] + k  # Update upper probability bound
        count += 1  # Move to next character
    m_final_listcheck.append(m_new)  # Store iteration result

# Error correction: Finding the most frequent value at each position
h = m_final_listcheck[0]
d = len(h)

m_final = []  # Stores final corrected message
for i in range(d):
    m_out = []  # Store all iterations for a position
    for j in range(len(m_final_listcheck)):
        m_out.append(m_final_listcheck[j][i])
    most_frequent = max(m_out, key=m_out.count)  # Get most common value
    m_final.append(most_frequent)  # Store corrected character code

print(m_final)  # Print corrected numerical sequence

# Convert numerical representation back to text
word = []
for i in range(len(m_final)):
    t = get_key_from_value(char_mapping, m_final[i])  # Map number to char
    word.append(t)  # Append to final output

word = ''.join(word)  # Convert list to string
print(word)  # Print final reconstructed string
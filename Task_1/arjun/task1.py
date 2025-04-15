import numpy as np
import math
from matrix import matrix

# Encoding and Decoding for the character set
CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVXYZ,.'

ENCODER = {char:i+1 for i, char in enumerate(CHARACTERS)}
DECODER = {i+1:char for i, char in enumerate(CHARACTERS)}

def encode(text):
    l = [ENCODER[char] for char in text]
    return l

def decode(code):
    l = [DECODER[char] for char in code]
    return ' '.join(l)

def channel_sim(text, matrix):
    # Simulate information transmission through the channel
    r, c = len(matrix), len(matrix[0])
    l = [np.random.choice(range(c), p=matrix[num]) for num in text]
    return l

def channel_capacity(matrix):
    # Given a matrix of P Y | X, C = max I(X, Y) for mentioned P(X)
    I = 0
    rows, columns = len(matrix), len(matrix[0])

    # Uniform distribution over entire matrix
    p_x = np.ones(rows)/rows

    # Multiply P Y|X by P(X) to get P(Y)
    p_y = np.dot(p_x, matrix)

    for i in range(rows):
        for j in range(columns):
            pyx = matrix[i][j]
            I += p_x[i]*pyx*math.log2(pyx)/p_y[j] if pyx > 0 else 0

    return -I

'''
'''

text = 'ARJUN.MINITASK'
code = encode(text)

print(code)
print(decode(code))

# Simulating information transmission
output = channel_sim(code, matrix)
ouput_obtained = decode(output)
print(ouput_obtained)

print(channel_capacity(matrix))

'''OUTPUT
[1, 18, 10, 21, 14, 27, 13, 9, 14, 9, 20, 1, 19, 11]
A R J U N . M I N I T A S K
B S K U M . N I M I T B T J
27.854812280691252
'''
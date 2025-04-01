import numpy as np
from math import log2

# Character set: A-Z (1-26), ,=27, .=28 (28 characters total)
CHAR_SET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ,.'  # Removed space from original set
ENCODE_MAP = {c: i+1 for i, c in enumerate(CHAR_SET)}
DECODE_MAP = {i+1: c for i, c in enumerate(CHAR_SET)}

def encode_text(text):
    """Convert text to numerical sequence"""
    return [ENCODE_MAP[c] if c in ENCODE_MAP else ENCODE_MAP['.'] 
            for c in text.upper().replace(' ', '_')]

def transmit(symbol, channel_matrix):
    """Simulate channel transmission for one symbol"""
    return np.random.choice(len(channel_matrix), 
                            p=channel_matrix[symbol-1])

def decode_sequence(sequence):
    """Convert numerical output back to text"""
    return ''.join([DECODE_MAP.get(num, '.') for num in sequence])

def simulate_channel(text, channel_matrix):
    """Simulate complete channel transmission"""
    encoded = encode_text(text)
    received = [transmit(s, channel_matrix) for s in encoded]
    return decode_sequence(received)

def channel_capacity(channel_matrix, max_iter=1000, tol=1e-10):
    """
    Compute channel capacity using Blahut-Arimoto algorithm
    channel_matrix: 2D array representing P(Y|X)
    """
    n_inputs, n_outputs = channel_matrix.shape
    
    # Initialize uniform input distribution
    p = np.ones(n_inputs) / n_inputs
    
    for _ in range(max_iter):
        # Compute q(y) = sum_x p(x)P(y|x)
        q = p @ channel_matrix
        
        # Avoid division by zero
        q = np.clip(q, 1e-16, 1.0)
        
        # Compute mutual information
        I = np.sum(p[:, None] * channel_matrix * 
                 np.log2(channel_matrix / q[None, :] + 1e-16))
        
        # Update input distribution
        p_new = p * np.exp(
            np.sum(channel_matrix * np.log2(channel_matrix / q[None, :] + 1e-16), 
                   axis=1)
        )
        p_new /= p_new.sum()
        
        # Check convergence
        if np.max(np.abs(p_new - p)) < tol:
            break
        p = p_new
    
    return I

def print_matrix(matrix):
    """Display channel matrix structure with row sums"""
    np.set_printoptions(precision=3, suppress=True)
    print("\nChannel Matrix Preview (first 10 rows/columns):")
    print(matrix[:10, :10])
    print("\nRow Sums Verification:")
    print(np.round(matrix.sum(axis=1), 3))

if __name__ == "__main__":
    # Create 28x28 channel matrix with specified pattern
    channel_matrix = np.zeros((28, 28))
    base_pattern = np.array([
        [0.7, 0.2, 0.1],
        [0.15, 0.05, 0.8],
        [0.15, 0.75, 0.1]
    ])
    
    # Apply pattern every 3 rows/columns with normalization
    for i in range(0, 27, 3):
        j = i  # Align columns with rows
        channel_matrix[i:i+3, j:j+3] = base_pattern
        
        # Normalize rows to sum to 1.0
        for row in range(i, i+3):
            row_sum = channel_matrix[row].sum()
            if row_sum > 0:
                channel_matrix[row] /= row_sum
    
    # Set final element (28,28) to 1.0
    channel_matrix[27, 27] = 1.0
    
    # Display matrix structure
    print_matrix(channel_matrix)
    
    # Run simulation
    input_text = input("\nEnter text:\t")
    output_text = simulate_channel(input_text, channel_matrix)
    
    # Calculate capacity
    capacity = channel_capacity(channel_matrix)
    
    print(f"\nOriginal: {input_text}")
    print(f"Received: {output_text}")
    print(f"Match: {input_text.upper() == output_text.replace('_', ' ')}")
    print(f"Channel Capacity: {capacity:.4f} bits/symbol")

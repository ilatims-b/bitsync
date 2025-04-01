"""
General Channel Matrix Simulator with Capacity Calculation
This program simulates text transmission through any valid channel matrix
and calculates the channel capacity using the Blahut-Arimoto algorithm.
"""

import numpy as np
from math import log2

# ----------------------
# Character Set Configuration
# ----------------------
# Define valid characters and their numerical mappings
# Format: A-Z (1-26), ', '=27, '.'=28, '_' (space)=29
CHAR_SET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ,._'  # 29 characters total

# Create encoding/decoding dictionaries
ENCODE_MAP = {c: i+1 for i, c in enumerate(CHAR_SET)}  # Character to numerical symbol
DECODE_MAP = {i+1: c for i, c in enumerate(CHAR_SET)}  # Numerical symbol to character

# ----------------------
# Core Functions
# ----------------------

def encode_text(text):
    """
    Convert input text to numerical symbols
    Args:
        text (str): Input text containing A-Z, ',', '.', and spaces
    Returns:
        list: Numerical sequence representing encoded text
    """
    return [ENCODE_MAP[c] if c in ENCODE_MAP else ENCODE_MAP['_']  # Default to space
            for c in text.upper().replace(' ', '_')]  # Case-insensitive, space->'_'

def transmit(symbol, channel_matrix):
    """
    Simulate transmission of a single symbol through the channel
    Args:
        symbol (int): Input symbol (1-based index)
        channel_matrix (np.array): Channel transition probability matrix
    Returns:
        int: Received symbol (0-based index)
    """
    return np.random.choice(channel_matrix.shape[0],  # Number of possible outputs
                            p=channel_matrix[symbol-1])  # Use row corresponding to input symbol

def decode_sequence(sequence):
    """
    Convert numerical output back to readable text
    Args:
        sequence (list): Received numerical symbols
    Returns:
        str: Decoded text with '_' converted to spaces
    """
    return ''.join([DECODE_MAP.get(num, '_') for num in sequence]).replace('_', ' ')

def simulate_channel(text, channel_matrix):
    """
    Complete transmission simulation pipeline
    Args:
        text (str): Input text to transmit
        channel_matrix (np.array): Channel transition matrix
    Returns:
        str: Received text after channel effects
    """
    encoded = encode_text(text)
    received = [transmit(s, channel_matrix) for s in encoded]
    return decode_sequence(received)

# ----------------------
# Channel Capacity Calculation
# ----------------------

def channel_capacity(channel_matrix, max_iter=1000, tol=1e-10):
    """
    Calculate channel capacity using Blahut-Arimoto algorithm
    Args:
        channel_matrix (np.array): Valid channel transition matrix
        max_iter (int): Maximum iterations for convergence
        tol (float): Tolerance for convergence check
    Returns:
        float: Channel capacity in bits per symbol
    """
    n = channel_matrix.shape[0]  # Number of input symbols
    p = np.full(n, 1/n)  # Initialize uniform input distribution
    I_prev = 0  # Previous mutual information value
    
    for _ in range(max_iter):
        # Compute output distribution q(y)
        q = np.clip(p @ channel_matrix, 1e-16, 1.0)  # Prevent numerical underflow
        
        # Calculate mutual information
        with np.errstate(divide='ignore', invalid='ignore'):
            log_ratios = np.log2(channel_matrix / q + 1e-16)
            I = np.sum(p[:, None] * channel_matrix * log_ratios)
        
        # Check for convergence
        if abs(I - I_prev) < tol:
            break
            
        # Update input distribution
        p = p * np.exp(np.sum(channel_matrix * log_ratios, axis=1))
        p /= p.sum()  # Normalize probabilities
        I_prev = I
    
    return I  # Return final mutual information (channel capacity)

# ----------------------
# Matrix Utilities
# ----------------------

def create_general_channel_matrix(n_symbols):
    """
    Generate valid random channel matrix
    Args:
        n_symbols (int): Number of input/output symbols
    Returns:
        np.array: Valid stochastic matrix (rows sum to 1)
    """
    matrix = np.random.rand(n_symbols, n_symbols)  # Uniform random values
    matrix /= matrix.sum(axis=1, keepdims=True)  # Normalize rows to sum to 1
    return matrix

def validate_channel_matrix(matrix):
    """
    Verify matrix is valid probability transition matrix
    Args:
        matrix (np.array): Proposed channel matrix
    Raises:
        ValueError: For invalid probability matrix
    """
    if not np.allclose(matrix.sum(axis=1), 1, atol=1e-8):
        raise ValueError("Invalid channel matrix: rows must sum to 1")
    if (matrix < 0).any() or (matrix > 1).any():
        raise ValueError("Matrix contains invalid probabilities (must be 0 ≤ p ≤ 1)")

# ----------------------
# Main Execution
# ----------------------

if __name__ == "__main__":
    # Configuration
    N_SYMBOLS = len(CHAR_SET)  # Number of symbols in our system
    
    try:
        # Create and validate channel matrix
        channel_matrix = create_general_channel_matrix(N_SYMBOLS)
        validate_channel_matrix(channel_matrix)
        
        # User interaction
        input_text = input("Enter text (A-Z, spaces, commas, periods):\t")
        output_text = simulate_channel(input_text, channel_matrix)
        
        # Capacity calculation
        capacity = channel_capacity(channel_matrix)
        
        # Display results
        print(f"\nOriginal text: {input_text}")
        print(f"Received text:  {output_text}")
        print(f"Channel capacity: {capacity:.4f} bits/symbol")
        
    except ValueError as e:
        print(f"Error: {str(e)}")


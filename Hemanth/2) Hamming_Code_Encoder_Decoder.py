import numpy as np

# Define Generator matrix G (4x7) and Parity-check matrix H (3x7)
G = np.array([
    [1, 0, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1]
])

H = np.array([
    [0, 1, 1, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 1]
])

# Syndrome to error-bit mapping
syndrome_table = {
    (0, 0, 0): None,
    (0, 0, 1): 6,
    (0, 1, 0): 5,
    (0, 1, 1): 2,
    (1, 0, 0): 4,
    (1, 0, 1): 0,
    (1, 1, 0): 1,
    (1, 1, 1): 3,
}

# Encoder: 4-bit → 7-bit
def encode_batch(data_bits):
    return np.dot(data_bits, G) % 2

# Decoder: 7-bit noisy input → 4-bit original message
def decode_batch(received_batch):
    decoded = []
    for received in received_batch:
        syndrome = tuple(np.dot(H, received.T) % 2)
        error_bit = syndrome_table.get(syndrome)
        corrected = received.copy()
        if error_bit is not None:
            corrected[error_bit] ^= 1  # flip the bit
        decoded.append(corrected[:4])  # extract data bits
    return np.array(decoded)

# Gaussian channel (adds noise then rounds and clips to binary)
def gaussian_channel(codewords, noise_std=0.5):
    noise = np.random.normal(0, noise_std, codewords.shape)
    received = codewords + noise
    return np.clip(np.round(received), 0, 1).astype(int)

# Uniform noise channel (bit flip with probability p)
def uniform_channel(codewords, flip_prob=0.1):
    flips = np.random.rand(*codewords.shape) < flip_prob
    return (codewords + flips.astype(int)) % 2

# Bit Error Rate (BER)
def bit_error_rate(original, decoded):
    total_bits = original.size
    errors = np.sum(original != decoded)
    return errors / total_bits

# Run simulation
def simulate(n=10, noise_std=0.5, flip_prob=0.1):
    messages = np.random.randint(0, 2, (n, 4))
    codewords = encode_batch(messages)

    # Gaussian Noise
    received_g = gaussian_channel(codewords, noise_std)
    decoded_g = decode_batch(received_g)
    ber_g = bit_error_rate(messages, decoded_g)

    # Uniform Noise
    received_u = uniform_channel(codewords, flip_prob)
    decoded_u = decode_batch(received_u)
    ber_u = bit_error_rate(messages, decoded_u)

    return {
        "Original": messages,
        "Encoded": codewords,
        "GaussianDecoded": decoded_g,
        "GaussianBER": ber_g,
        "UniformDecoded": decoded_u,
        "UniformBER": ber_u
    }

# Example usage
if __name__ == "__main__":
    np.random.seed(42)  # Reproducibility
    results = simulate(n=100, noise_std=0.5, flip_prob=0.2)
    print("🎬 Simulation Starts:")

    # Running the simulation
    print(f"🔄 Running Simulation over {len(results['Original'])} messages...\n-----------------------------------------------------")

    # Show first 3 messages
    print(f"🔢 First 3 Messages:\n")
    print("💬 Original Messages:\n", results["Original"][:3])
    print("-----------------------------------------------------\n🔑 Encoded Codewords:\n", results["Encoded"][:3])

    # Gaussian Decoding and BER
    print("-----------------------------------------------------\n📡 Gaussian Decoded:\n", results["GaussianDecoded"][:3])
    print("📉 Bit Error Rate (Gaussian):", results["GaussianBER"])

    # Uniform Decoding and BER
    print("-----------------------------------------------------\n📦 Uniform Decoded:\n", results["UniformDecoded"][:3])
    print("📉 Bit Error Rate (Uniform):", results["UniformBER"])
    print("-----------------------------------------------------\n🎬 Simulation Ends.")

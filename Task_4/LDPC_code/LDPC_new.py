import numpy as np
from itertools import combinations
import random

class LDPCEncoder:
    def __init__(self, k):
        self.k = k
        self.G, self.H = self.construct_generator_and_parity_check()

    def construct_generator_and_parity_check(self):
        subsets = []
        for r in range(self.k, 0, -1):
            subsets.extend(list(combinations(range(self.k), r)))

        n = len(subsets)
        G_full = np.zeros((self.k, n), dtype=int)
        for col_idx, subset in enumerate(subsets):
            for row_idx in subset:
                G_full[row_idx][col_idx] = 1

        P = G_full[:, :-self.k]
        I_k = G_full[:, -self.k:]
        assert np.array_equal(I_k, np.identity(self.k, dtype=int)), "Last k columns of G are not identity."

        G = np.concatenate((P, I_k), axis=1)
        H = np.concatenate((np.identity(n - self.k, dtype=int), P.T), axis=1)

        return G, H

    def encode(self, message):
        return message @ self.G % 2


class BinaryErasureChannel:
    def __init__(self, erasure_prob=0.1):
        self.erasure_prob = erasure_prob

    def transmit(self, codeword):
        received = []
        for bit in codeword:
            if random.random() < self.erasure_prob:
                received.append('e')  # 'e' for erased
            else:
                received.append(str(bit))
        return received


class LDPCDecoder:
    def __init__(self, H):
        self.H = H

    def decode(self, received):
        n = len(received)
        codeword = [None if bit == 'e' else int(bit) for bit in received]
        codeword = np.array(codeword, dtype=object)

        max_iterations = 100
        for _ in range(max_iterations):
            updated = False
            for row in self.H:
                indices = [i for i, bit in enumerate(row) if bit == 1]
                involved = [codeword[i] for i in indices]

                unknown_indices = [i for i, bit in zip(indices, involved) if bit is None]
                known_values = [bit for bit in involved if bit is not None]

                if len(unknown_indices) == 1:
                    known_sum = sum(known_values) % 2
                    missing_idx = unknown_indices[0]
                    codeword[missing_idx] = known_sum
                    updated = True

            if not updated:
                break

        for i in range(len(codeword)):
            if codeword[i] is None:
                print(f" Warning: Bit at index {i} could not be recovered. Defaulting to 0.")
                codeword[i] = 0

        return np.array(codeword, dtype=int)


class CodewordComparator:
    @staticmethod
    def compare(original, decoded):
        return "Success" if np.array_equal(original, decoded) else "Failure"


# === Main Execution ===
q = int(input("Enter the length of your message chunks (q): \n"))
msg_input = input("Enter the message (as a binary number, e.g., 1011): \n")
epsilon = 0.1  # BEC erasure probability

# Message preprocessing
message = np.array([int(bit) for bit in msg_input.strip()], dtype=int)
assert len(message) == q, f"Message length ({len(message)}) must match q = {q}"

# Instantiate and use classes
encoder = LDPCEncoder(q)
codeword = encoder.encode(message)

bec = BinaryErasureChannel(epsilon)
received = bec.transmit(codeword)

decoder = LDPCDecoder(encoder.H)
decoded_codeword = decoder.decode(received)

# Output
print(f"\n Generator matrix G = [P | I] (shape {encoder.G.shape}):\n{encoder.G}")
print(f"\n Parity-check matrix H = [I | P^T] (shape {encoder.H.shape}):\n{encoder.H}")
print(f"\n Original message: {message}")
print(f" Encoded codeword: {codeword}")
print(f" Received over BEC(ε={epsilon}): {received}")
print(f"\n Decoded codeword: {decoded_codeword}")
print(CodewordComparator.compare(codeword, decoded_codeword))

"""
Simulates a basic communication channel using a Markov chain.
The channel is represented by a transition probability matrix, where each state corresponds to a character in the alphabet.
The input text is encoded into numerical values, passed through the channel, and then decoded back into text.
The channel simulates the probability of transitioning from one character to another, allowing for the introduction of errors in the transmitted message.
Create a custom encoding scheme to improve the performance of the channel.
"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def encode_alphabet_naive(text):
    encoded_values = []
    for char in text:
        char = char.lower()
        if char == ' ':
            encoded_values.append(27)
        elif char == '.':
            encoded_values.append(28)
        elif char.isalpha():
            encoded_values.append(ord(char) - ord('a') + 1)
        else:
            encoded_values.append(char)  # Keep non-alphabet characters unchanged
    return encoded_values

def encode_alphabet_custom(text):
    encoded_values = []
    for char in text:
        char = char.lower()
        if char == ' ':
            encoded_values.append(27)
        elif char == '.':
            encoded_values.append(28)
        elif char.isalpha():
            encoded_values.append(ord(char) - ord('a') + 1)
        else:
            encoded_values.append(char)  # Keep non-alphabet characters unchanged
    encoded_values = [
    x if x % 3 == 1 else 
    (x + 1 if x % 3 == 2 else x - 1) 
    for x in encoded_values
    ] # Custom encoding logic
    return encoded_values 

def decode_alphabet(encoded_values):
    decoded_text = ""
    for num in encoded_values:
        if num == 27:
            decoded_text += ' '
        elif num == 28:
            decoded_text += '.'
        elif 1 <= num <= 26:
            decoded_text += chr(ord('a') + num - 1)  # Convert back to lowercase letter
        else:
            decoded_text += str(num)  # Keep unchanged for unexpected values
    return decoded_text

def random_out(pdist):
    return np.random.choice(np.arange(1, len(pdist) + 1), p=pdist)

def plot_channel_matrix(probab_matrx):
    # Plot heatmap
    plt.figure(figsize=(10, 7))
    # Create a custom orange color palette
    orange_palette = sns.light_palette("orange", as_cmap=True)

    # Plot the heatmap with the custom palette
    ax = sns.heatmap(probab_matrx, cmap=orange_palette, cbar=True)

    # Axis labels
    ax.set_ylabel("Input", fontsize=16)
    ax.yaxis.set_label_position("left")
    ax.set_xlabel("")  # Hide default xlabel

    # Add horizontal axis label on top
    ax_top = ax.twiny()
    ax_top.set_xlim(ax.get_xlim())
    ax_top.set_xticks(ax.get_xticks())
    ax_top.set_xticklabels(ax.get_xticklabels())
    ax_top.set_xlabel("Output", fontsize=14)
    plt.title("Channel Matrix", fontsize=18)
    plt.show()

def mean_squared_error(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)
    return np.mean((actual - predicted) ** 2)

probab_matrx = np.array([
[0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # pdf(output|input = 1)
[0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # pdf(output|input = 2)
[0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # pdf(output|input = 3)
[0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # pdf(output|input = 4)
[0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # pdf(output|input = 5)
[0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.2, 0.1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.05, 0.8, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.75, 0.1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
])

# Normalize each row and column
probab_matrx = probab_matrx / probab_matrx.sum(axis=1, keepdims=True)
probab_matrx = probab_matrx / probab_matrx.sum(axis=0, keepdims=True)

plot_channel_matrix(probab_matrx)
"""
From the plot, we see that for the most optimal encoding, we have to swap the encoding of (1,2), (4,5), (7,8), (10,11), (13,14), (16,17), (19,20), (22,23), (25,26) and the others as it is.
In this way, we can increase the chances of getting a better output.
"""

m = probab_matrx.shape[0]
n = probab_matrx.shape[1]

for i in range(m):
    probab_matrx[i] = probab_matrx[i] / np.sum(probab_matrx[i])
# Input text
input_text = "abcdefghijklmnopqrstuvwxyz"
print(f"📡 Channel Simulation 📡\n")
print(f"🔤 input_text = {input_text}\n-----------------------------------------------------------------------------------------")
print(f"📝 With the naive encoding, we have the following encoding:")

# Naive Encoding
encoded_text_naive = encode_alphabet_naive(input_text)
print(f"📜 encoded_text_naive = {encoded_text_naive}")

# Random choice based on probability matrix
output_naive = []
for i in range(len(encoded_text_naive)):
    x = encoded_text_naive[i]
    y = random_out(probab_matrx[x - 1])
    output_naive.append(y)

output_naive = [x.item() for x in output_naive]
print(f"🔢 output of the naive encoding = {output_naive}")

# Decoding the output_naive
decoded_text = decode_alphabet(output_naive)
print(f"🔄 decoded_text = {decoded_text}")
# Calculate MSE between naive encoding output and the actual naive encoding
mse_naive = mean_squared_error(encoded_text_naive, output_naive)
print(f"📉 Mean Squared Error (Naive) = {mse_naive}\n-----------------------------------------------------------------------------------------")

# Custom Encoding
print(f"✨ With the custom encoding, we have the following encoding:")
encoded_text_custom = encode_alphabet_custom(input_text)
print(f"📜 encoded_text_custom = {encoded_text_custom}")

# Random choice based on probability matrix for custom encoding
output_custom = []
for i in range(len(encoded_text_custom)):
    x = encoded_text_custom[i]
    y = random_out(probab_matrx[x - 1])
    output_custom.append(y)

output_custom = [x.item() for x in output_custom]
print(f"🔢 output of the custom encoding = {output_custom}")

# Decoding the custom encoding
decoded_text = decode_alphabet(output_custom)
print(f"🔄 decoded_text = {decoded_text}")
# Calculate MSE between custom encoding output and the actual naive encoding
mse_custom = mean_squared_error(encoded_text_naive, output_custom)
print(f"📉 Mean Squared Error (Custom) = {mse_custom}\n-----------------------------------------------------------------------------------------")
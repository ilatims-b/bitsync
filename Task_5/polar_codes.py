"""
Developer : EE24B069
Date : 24 April 2025
Purpose : To implement polar codes
Inputs : -
Outputs :   Encoded message list1
            Zero padded message list
            Decoded message list
            Rate
            Probability of bit error
"""

import numpy as np
from copy import deepcopy

def gaussian_channel_simulator(encoded_message_arr, std_dev_of_error):      #simulaates gaussian channel
    modulated_arr = (2 * encoded_message_arr) - 1
    return np.random.normal(0, std_dev_of_error, modulated_arr.shape) + modulated_arr

def worst_to_best_channel_indices_arr_reducer(no_of_channels, worst_to_best_channel_indices_arr):       #gives a new_worst_to_best_channel_indices_arr that is contains values from 0 to no_of_channels-1
    if no_of_channels > worst_to_best_channel_indices_arr.shape[0]:
        print("need more data for ordering the inputs")
        return None
    elif no_of_channels == worst_to_best_channel_indices_arr.shape[0]:
        new_worst_to_best_channel_indices_arr = worst_to_best_channel_indices_arr.copy()
    else:
        new_worst_to_best_channel_indices_arr = np.zeros((no_of_channels,), dtype="int32")
        count = 0
        index = 0
        while count < no_of_channels:
            if worst_to_best_channel_indices_arr[index] < no_of_channels:
                new_worst_to_best_channel_indices_arr[count] = worst_to_best_channel_indices_arr[index]
                count += 1
            index += 1
    return  new_worst_to_best_channel_indices_arr

def channel_inputs_organiser(depth_of_tree, worst_to_best_channel_indices_arr, message_list):               #puts frozen bits as zeros
    no_of_channels = 2**depth_of_tree                                       #implemented by first padding zeros to the front of the message list and then
    new_worst_to_best_channel_indices_arr = worst_to_best_channel_indices_arr_reducer(no_of_channels, worst_to_best_channel_indices_arr)
    no_of_zeros_to_be_padded = no_of_channels - len(message_list)           #then the inputs are interleaved according to worst_to_best_channel_indices_arr
    new_message_list = [0]*no_of_zeros_to_be_padded
    new_message_list.extend(message_list)
    order_arranged_message_list = [0]*no_of_channels
    for i, message_bit in enumerate(new_message_list):
        order_arranged_message_list[new_worst_to_best_channel_indices_arr[i]] = new_message_list[i]
    return order_arranged_message_list

def polar_operation(list1, list2):      #it returns a list comprising list1^list2, list2
    new_list = list1.copy()
    for i in range(len(list1)):
        new_list[i] = list1[i]^list2[i]
    new_list.extend(list2)
    return new_list

def polar_encoder(depth_of_tree, worst_to_best_channel_indices_arr, message_list):      #polar encoder, could handle chunks of messages, len(message_list)<no_of_channels
    no_of_channels = 2**depth_of_tree
    organised_channel_input_list = channel_inputs_organiser(depth_of_tree, worst_to_best_channel_indices_arr, message_list)
    nested_list = []
    for i in range(no_of_channels):
        nested_list.append(organised_channel_input_list[i:i+1])
    while len(nested_list) > 1:
        new_nested_list = []
        for i in range(0, len(nested_list), 2):
            new_nested_list.append(polar_operation(nested_list[i], nested_list[i+1]))
        nested_list = deepcopy(new_nested_list)
    return nested_list[0]


class Node:         #Node in the tree, implementing Successive Cancellation Decoder of polar code
    def __init__(self, depth, position, depth_of_tree, llr_list, parent_node):
        self.position = position
        self.depth = depth
        self.depth_of_tree = depth_of_tree
        self.next_step = "send info to left child"
        self.parent_node = parent_node
        self.llr_list = llr_list
        self.half_of_no_of_leaves_below = 2**(depth_of_tree - depth - 1)
        self.no_of_leafs_below = 2 * self.half_of_no_of_leaves_below
        self.bits_list_received_from_left_child = []
        self.bits_list_received_from_right_child = []
        self.bits_list_to_be_sent_above = []

    def minsum_calculater(self):  #approximating log sum exp by minsum
        llr1 = np.array(self.llr_list[:self.half_of_no_of_leaves_below])
        llr2 = np.array(self.llr_list[self.half_of_no_of_leaves_below:])
        new_llr_arr = -1 * np.sign(llr1) * np.sign(llr2) * np.minimum(np.abs(llr1), np.abs(llr2))
        return list(new_llr_arr)

    def llr_for_right_child_calculator(self):  #
        llr1 = np.array(self.llr_list[:self.half_of_no_of_leaves_below])
        llr2 = np.array(self.llr_list[self.half_of_no_of_leaves_below:])
        bits_arr = np.array(self.bits_list_received_from_left_child)
        return list(llr2 + (1-2*bits_arr)*llr1)

    def create_and_send_info_to_left_child(self):       #creates left child node,send it llrs and returns it
        if self.depth != self.depth_of_tree:
            left_child_node = Node(self.depth+1, 2*self.position, self.depth_of_tree, self.minsum_calculater(), self)
            self.next_step = "send info to right child"
            return left_child_node
        else:       #if the node is a leaf
            self.next_step = "send info above"
            return self

    def create_and_send_info_to_right_child(self):   #creates right child node,send it llrs and returns it
        if self.depth != depth_of_tree1:
            right_child_node = Node(self.depth + 1, 2 * self.position + 1, self.depth_of_tree, self.llr_for_right_child_calculator(), self)
            self.next_step = "send info above"
            return right_child_node
        else:       #if the node is a leaf
            self.next_step = "send info above"
            return self

    def send_info_above(self, frozen_indices_list, decoded_message_arr_with_zero_padding):    #sends the decoded bits above  #
        if self.depth_of_tree != self.depth:
            self.bits_list_to_be_sent_above = polar_operation(self.bits_list_received_from_left_child, self.bits_list_received_from_right_child)
        elif (self.position in frozen_indices_list) or (self.llr_list[0] < 0):
            self.bits_list_to_be_sent_above = [0]
            decoded_message_arr_with_zero_padding.append(0)
        else:
            self.bits_list_to_be_sent_above = [1]
            decoded_message_arr_with_zero_padding.append(1)
        if self.position % 2 == 0:
            self.parent_node.bits_list_received_from_left_child = self.bits_list_to_be_sent_above
        else:
            self.parent_node.bits_list_received_from_right_child = self.bits_list_to_be_sent_above
        self.next_step = "nothing left"
        return self.parent_node

    def __eq__(self, other):
        if (self.depth == other.depth) and (self.position == other.position):
            return True
        else:
            return False

def frozen_bits_remover(decoded_message_list, new_worst_to_best_channel_indices_arr, no_of_channels_used_for_message_bits, no_of_channels):     #deinterleaves the decoded message list and then removes starting zeros
    no_of_padded_zeros = no_of_channels - no_of_channels_used_for_message_bits
    reordered_message_list = [0]*no_of_channels
    for i, value in enumerate(new_worst_to_best_channel_indices_arr):
         reordered_message_list[i] = decoded_message_list[new_worst_to_best_channel_indices_arr[i]]
    #print(reordered_message_list)
    return reordered_message_list[no_of_padded_zeros:]
        
def polar_decoder(received_list, depth_of_tree, worst_to_best_channel_indices_arr, no_of_channels_used_for_message_bits):       #polar decoder but could only handle one chunk
    no_of_channels = 2**depth_of_tree
    new_worst_to_best_channel_indices_arr = worst_to_best_channel_indices_arr_reducer(no_of_channels,
                                                                                      worst_to_best_channel_indices_arr)
    frozen_indices_list = list(new_worst_to_best_channel_indices_arr[:no_of_channels - no_of_channels_used_for_message_bits])
    decoded_message_list_with_zero_padding = []
    start_node = Node(0, 0, depth_of_tree, received_list, None)
    current_node = start_node
    while (current_node != start_node) or (start_node.next_step != "send info above"):
        #print(current_node.depth, current_node.position, current_node.next_step, current_node.llr_list)
        if current_node.next_step == "send info to left child":
            current_node = current_node.create_and_send_info_to_left_child()
        elif current_node.next_step == "send info to right child":
            current_node = current_node.create_and_send_info_to_right_child()
        elif current_node.next_step == "send info above":
            current_node = current_node.send_info_above(frozen_indices_list, decoded_message_list_with_zero_padding)
        else:
            print("something went wrong")
            break
    return frozen_bits_remover(decoded_message_list_with_zero_padding, new_worst_to_best_channel_indices_arr, no_of_channels_used_for_message_bits, no_of_channels)        #removes frozen bits

def complete_polar_encoder(message_list, depth_of_tree, no_of_channels_used_for_message_bits, worst_to_best_channel_indices_arr):       #more generalised polar encoder, breaks bigger messages into smaller parts and sends it to polar encoder
    no_of_channels = 2**depth_of_tree
    new_worst_to_best_channel_indices_arr = worst_to_best_channel_indices_arr_reducer(no_of_channels, worst_to_best_channel_indices_arr)
    no_of_info_bits_without_zero_padding = len(message_list)
    no_of_chunks = no_of_info_bits_without_zero_padding//no_of_channels_used_for_message_bits
    if no_of_chunks*no_of_channels_used_for_message_bits != no_of_info_bits_without_zero_padding:
        no_of_chunks += 1
        no_of_extra_zeros_to_be_appended = no_of_chunks*no_of_channels_used_for_message_bits - no_of_info_bits_without_zero_padding
        message_list.extend([0]*no_of_extra_zeros_to_be_appended)
    encoded_message_list = []
    start_index = 0
    end_index = 0
    for i in range(no_of_chunks):
        end_index += no_of_channels_used_for_message_bits
        encoded_message_list.extend(
            polar_encoder(depth_of_tree, new_worst_to_best_channel_indices_arr, message_list[start_index:end_index]))
        start_index = end_index
    return encoded_message_list

def complete_polar_decoder(received_arr, depth_of_tree, no_of_channels_used_for_message_bits, worst_to_best_channel_indices_arr):   #more generalised polar decoder, breaks bigger messages into smaller chunks and sends it to polar decoder
    no_of_channels = 2 ** depth_of_tree
    new_worst_to_best_channel_indices_arr = worst_to_best_channel_indices_arr_reducer(no_of_channels,
                                                                                      worst_to_best_channel_indices_arr)
    
    no_of_chunks = received_arr.shape[0]//no_of_channels
    start_index = 0
    end_index = 0
    final_decoded_list = []
    for i in range(no_of_chunks):
        end_index += no_of_channels
        final_decoded_list.extend(polar_decoder(list(received_arr[start_index:end_index]), depth_of_tree, new_worst_to_best_channel_indices_arr, no_of_channels_used_for_message_bits))
        start_index = end_index
    return final_decoded_list

def no_of_bit_errors_finder(message_list, decoded_message_list):        #finds the number of differences in two iterables
    no_of_bit_errors = 0
    for i in range(len(message_list)):
        if message_list[i] != decoded_message_list[i]:
            no_of_bit_errors += 1
    return no_of_bit_errors

std_dev_of_error1 = 1.0
depth_of_tree1 = 5
no_of_channels_used_for_message_bits1 = 8
no_of_message_bits1 = 1000
message_list1 = list(np.random.randint(0,2,no_of_message_bits1))
worst_to_best_channel_indices_arr1 = np.array([1,2,3,5,9,17,4,6,10,7,18,11,19,13,21,25,8,12,20,14,15,22,27,26,23,29,16,24,28,30,31,32], dtype="int32") - 1
encoded_message_list1 = complete_polar_encoder(message_list1, depth_of_tree1, no_of_channels_used_for_message_bits1, worst_to_best_channel_indices_arr1)
print("Encoded message list1 :", encoded_message_list1)
received_arr1 = gaussian_channel_simulator(np.array(encoded_message_list1), std_dev_of_error1)
decoded_message_list1 = complete_polar_decoder(received_arr1, depth_of_tree1, no_of_channels_used_for_message_bits1, worst_to_best_channel_indices_arr1)
print("Zero padded message list :", message_list1)
print("Decoded message list     :", decoded_message_list1)
print("Rate :", no_of_channels_used_for_message_bits1/(2**depth_of_tree1))
print("Probability of bit error :", no_of_bit_errors_finder(message_list1, decoded_message_list1)/no_of_message_bits1)

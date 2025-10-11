import sys

# Class to represent each position in the hash table
class Slot:
    def __init__(self):
        self.key = None # Stores the key 
        self.status = "never used"  # Initial state of each slot is "never used" but can also be "occupied" or "tombstone"

# Class to represent entire hash table
class HashTable:
    def __init__(self):
        self.table = [] # Initialise hash table
        for _ in range(26): # Create 26 slots for each letter of the alphabet
            self.table.append(Slot())   # Append new slot to the table

    def hash_get(self, key):    # Hash function to get index using the last character of the word
        return ord(key[-1]) - ord('a')  # Converts last character to its ASCII value and maps it to 0 - 25
    
    def find(self, key):    # Function to find index of a key in the hash table
        start_index = self.hash_get(key)    # Get starting index using above function
        i = start_index # Begins searching from the hashed index
        while True: # Loops until key is found or empty slot is encountered
            slot = self.table[i]    # Get the slot at i 
            if slot.status == "never used": # If slot is never used, key is not there
                return -1
            elif slot.status == "occupied" and slot.key == key: # If slot is occupied and key is found, return index
                return i
            i = (i + 1) % 26    # Move to next slot, wrapping around if necessary
            if i == start_index:    # If we have looped all the way back to the start, key is not there
                return -1
            
    def insert(self, key):  # Function to insert a key into the hash table
        if self.find(key) != -1:    # If key already exists do nothing
            return
        
        start_index = self.hash_get(key)    # Get starting index using hash function
        i = start_index # Begins searching from the hashed index
        while True: # Loops until an empty or tombstone slot is found
            slot = self.table[i]    # Get the slot at i
            if slot.status != "occupied":   # If slot is empty or a tombstone, insert key 
                slot.key = key
                slot.status = "occupied"    # Set the slot to occupied
                return
            i = (i + 1) % 26    # Move to next slot, wrapping around if necessary
            if i == start_index:    # If we have looped all the way back to the start, stop as table is full
                return
            
    def delete(self, key):  # Function to delete a key from the hash table
        index = self.find(key)  # Find the index of the key
        if index != -1: # If the key is found, mark it as a tombstone
            self.table[index].status = "tombstone" 
            self.table[index].key = None    # Clear the key

    def collect_keys(self): # Function to collect all occupied keys in slot order
        result = [] # Initialise list to store keys
        for slot in self.table: # Iterates through each slot in the hash table
            if slot.status == "occupied":   # If slot is occupied, add the key to the result list
                result.append(slot.key)
        return result
    
# Main code
if __name__ == "__main__":
    inputs = sys.stdin.readline().strip().split()    # Read input and split into list of inputs
    hash_table = HashTable()    # Create new hash table

    for item in inputs:  # Iterate through each input
        if not inputs:  # If input is empty, skip
            continue
        operation = item[0]   # First character in array is the operation
        word = item[1:]   # The remaining characters in array are the word
        if operation == "A":    # If operation is "A", insert word into hash table
            hash_table.insert(word)
        elif operation == "D":  # If operation is "D", delete word from hash table
            hash_table.delete(word)

    print (" ".join(hash_table.collect_keys())) # Print all occupied keys in slot order seperated by spaces
# Name:  Doug Leedke
# OSU Email: leedked@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 3/18/2023
# Description: An implementation of a HashMap utilizing chaining.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the given key/value pair in the hash map.  If the given key already exists
        it's value will be replaced with the one provided.  Otherwise if it does not, a new
        key/value pair will be added to the hash map.
        """

        # Checking for resize
        if(self.table_load() >= 1):
            self.resize_table(self._capacity * 2)
        
        # Hashing the key to get the index inside our current capacity
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Reference to the bucket the key should be in
        bucket = self._buckets[index]
        
        found = False

        # Iterating the linked list to check for the key
        for node in bucket:

            # Key found, replacing old value with new
            if(node.key == key):
                found = True
                node.value = value
                break

        # Key not found inserting into bucket
        if found == False:
            bucket.insert(key, value)
            self._size += 1


    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        
        empty = 0

        # Iterating buckets and checking the length of the linked lists to determine
        # if they are empty
        for i in range(0, self._buckets.length()):
            if(self._buckets[i].length() == 0):
                empty += 1

        return empty


    def table_load(self) -> float:
        """
        This method returns the current table load factor (# of elements / # of buckets).
        """

        return self._size / self._buckets.length()

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. 
        """

        for i in range(0, self._buckets.length()):
            self._buckets[i] = LinkedList()

        self._size = 0


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table to the provided capacity.  If the capacity
        given is not a prime number, the new capacity will be set to be the next prime number after
        the given new capacity.
        """

        # Capacity must be >= 1
        if(new_capacity < 1):
            return
        
        # Checking if prime, otherwise getting the next prime
        if(self._is_prime(new_capacity) == False):
            new_capacity = self._next_prime(new_capacity)

        # Saving the old buckets 
        old_buckets = self._buckets

        # Creating a new array, setting new_capacity, resetting size
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        # Filling the new buckets with empty linked lists
        while self._buckets.length() < new_capacity:
            self._buckets.append(LinkedList())

        # Iterating old buckets
        for i in range(0, old_buckets.length()):

            # If there are elements in the bucket
            if(old_buckets[i].length() > 0):

                # Iterating the bucket's nodes and rehashing into the new hash map
                for ele in old_buckets[i]:
                    self.put(ele.key, ele.value)

    def get(self, key: str):
        """
        This method returns the value associated with the given key.  If the
        key is not in the hash map, the method returns None.
        """
    
        # Hashing the key to get the index inside our current capacity
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Reference to the bucket the key should be in
        bucket = self._buckets[index]
        
        # Iterating the linked list to check for the key
        for node in bucket:

            # Key found, return value
            if(node.key == key):
                return node.value
            
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        """

        # Empty hash map, no keys
        if(self._size == 0):
            return False

        # Getting index & bucket reference
        hash = self._hash_function(key) % self._capacity
        index = hash % self._capacity
        bucket = self._buckets[index]

        # Checking bucket for key
        if(bucket.contains(key) is not None):
            return True
        
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method will do nothing.
        """

        # Getting index & bucket reference
        hash = self._hash_function(key) % self._capacity
        index = hash % self._capacity
        bucket = self._buckets[index]

        if(bucket.remove(key)):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a 
        key/value pair stored in the hash map.
        """

        result = DynamicArray()

        # Iterating buckets
        for i in range(0, self._buckets.length()):

            # Checking if bucket has nodes
            if(self._buckets[i].length() != 0):

                # Iterating nodes and appending key/value tuple to DA
                for node in self._buckets[i]:
                    result.append((node.key, node.value))

        return result


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Function that receives a DynamicArray and returns a tuple containing a
    DynamicArray comprising the mode (most occurring) value/s of the array 
    and an integer that represents the highest frequency.  If there is more 
    than one value with the highest frequency, all of the values will be included
    in the array.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    result_da = DynamicArray()

    # Iterating array, filling hash map with each key and its frequency
    for i in range(0, da.length()):
        
        if(map.contains_key(da[i])):
            # Key exists already, incrementing the value
            map.put(da[i], map.get(da[i]) + 1)
        else:
            # Key does not exists, adding w/ value of 1
            map.put(da[i], 1)

    # Gettings list of all keys and values into an array
    counts = map.get_keys_and_values()
    max_freq = 0

    # Iterating to find the max frequency
    for i in range(0, counts.length()):
        if(counts[i][1] > max_freq):
            max_freq = counts[i][1]

    # Iterating to fill the result array with the max frequency keys
    for i in range(0, counts.length()):
        if(counts[i][1] == max_freq):
            result_da.append(counts[i][0])

    return (result_da, max_freq)

    

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)
    
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
    
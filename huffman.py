from ordered_list import *
from huffman_bit_writer import *
from huffman_bit_reader import *


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  # stored as an integer - the ASCII character code value
        self.freq = freq  # the freqency associated with the node
        self.left = None  # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        return type(other) == HuffmanNode and self.freq == other.freq and self.char == other.char

    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if type(other) == HuffmanNode and self.freq < other.freq:
            return True
        if type(other) == HuffmanNode and self.freq == other.freq and self.char < other.char:
            return True
        return False


def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    try:
        with open(filename, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        raise FileNotFoundError

    freq = [0] * 256

    for character in text:
        ascii_value = ord(character)
        freq[ascii_value] = int(freq[ascii_value]) + 1

    return freq


def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    lst = OrderedList()
    index = 0
    for freq in char_freq:
        new = HuffmanNode(index, freq)
        # print(new.freq)
        # print(new.char)
        if freq > 0:
            lst.add(new)
        index += 1
    if lst.is_empty():
        return None
    while lst.size() > 1:
        x = lst.pop(0)
        y = lst.pop(0)
        newfreq = x.freq + y.freq
        if x.char < y.char:
            new = HuffmanNode(x.char, newfreq)
            new.left = x
            new.right = y
        elif y.char < x.char:
            new = HuffmanNode(y.char, newfreq)
            new.left = x
            new.right = y
        lst.add(new)
    root = lst.pop(0)
    return root

    # print(lst.python_list())
    # print(lst.index(HuffmanNode(0, 2)))
    # print(lst.index(HuffmanNode(5, 2)))
    # print(lst.index(HuffmanNode(1, 4)))
    # print(lst.index(HuffmanNode(2, 8)))
    # print(lst.index(HuffmanNode(8, 16)))
    # print(lst.index(HuffmanNode(3, 16)))
    # print(lst.search(HuffmanNode(4, 0)))


def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    result = [''] * 256
    value = ''
    if node is None:
        return result
    create_code_helper(node, value, result)
    return result


def create_code_helper(node, value, result):
    if node.left is None and node.right is None:
        result[node.char] = value
        return
    if node.left is not None:
        create_code_helper(node.left, value + "0", result)
    if node.right is not None:
        create_code_helper(node.right, value + "1", result)


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    header = ''
    index = 0
    for freq in freqs:
        if freq > 0:
            header = header + str(index) + " " + str(freq) + " "
        index += 1
    return header.rstrip()


def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    try:
        with open(in_file, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        raise FileNotFoundError

    char_freq = cnt_freq(in_file)
    node = create_huff_tree(char_freq)
    huffman_array = create_code(node)
    header = create_header(char_freq)

    encoded = ''
    for character in text:
        encoded += huffman_array[ord(character)]

    output = open(out_file, 'w')
    if header != '':
        output.write(header + "\n")
    output.write(encoded)
    output.close()

    filename = str(out_file)
    c_file = filename[:-4] + "_compressed.txt"

    bit_object = HuffmanBitWriter(c_file)
    bit_object.write_str(header)
    if header != '':
        bit_object.write_str("\n")
    bit_object.write_code(encoded)
    bit_object.close()
    file.close()


def huffman_decode(encoded_file, decode_file):
    try:
        with open(encoded_file, 'r') as file:
            file.close()
    except FileNotFoundError:
        raise FileNotFoundError

    bit_object = HuffmanBitReader(encoded_file)
    header = bit_object.read_str()
    list_of_freqs = parse_header(header)

    node = create_huff_tree(list_of_freqs)
    result = ''
    num_c = total(header)
    root = node

    while len(result) < num_c:
        if len(header.split()) > 2:
            bit = bit_object.read_bit()
            if node.left is None and node.right is None:
                result += chr(node.char)
                node = root
            if bit is False:
                node = node.left
            if bit is True:
                node = node.right
        else:
            result += chr(node.char) * num_c

    output = open(decode_file, 'w')
    output.write(result)
    output.close()
    bit_object.close()


def parse_header(header_string):
    freq = [0] * 256
    header_list = list(header_string.split())
    for i in range(0, len(header_list), 2):
        freq[int(header_list[i])] = int(header_list[i + 1])
    return freq


def total(header_string):
    sum = 0
    freq_list = list(header_string.split())
    for i in range(1, len(freq_list), 2):
        sum += int(freq_list[i])
    return sum

# testlist = "dddddd ccccffaa"
# for character in testlist:
#     print(character)
#
# y = ord(' ')
# print(y)

# testlist2 = [2, 4, 8, 16, 0, 2, 0, 1, 16]
# create_huff_tree(testlist2)


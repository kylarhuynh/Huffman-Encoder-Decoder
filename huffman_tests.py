import unittest
import filecmp
import subprocess
from ordered_list import *
from huffman import *


class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)

    def test_cnt_freq_space(self):  # tests a file with just one space character
        freqlist = cnt_freq("1space.txt")
        anslist = [1]
        self.assertListEqual(freqlist[32:33], anslist)

    def test_cnt_freq_error(self):  # Raise FileNotFound error
        with self.assertRaises(FileNotFoundError):
            cnt_freq("notafile.txt")

    def test_cnt_freq_empty(self):  # empty
        freqlist = cnt_freq('empty.txt')
        anslist = [0] * 256
        self.assertEqual(freqlist, anslist)

    def test_lt_and_eq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        ascii = 97
        lst = OrderedList()
        for freq in anslist:
            node = HuffmanNode(ascii, freq)
            lst.add(node)
            ascii += 1
        self.assertEqual(lst.index(HuffmanNode(101, 0)), 0)
        self.assertEqual(lst.index(HuffmanNode(100, 16)), 6)
        self.assertEqual(lst.index(HuffmanNode(97, 2)), 2)
        self.assertFalse(HuffmanNode(97, 2) == None)

    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

    def test_create_huff_tree_1(self):  # test 1 entry
        freqlist = cnt_freq("1space.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 1)

    def test_create_huff_tree_empty(self):  # test empty
        freqlist = cnt_freq("empty.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree, None)

    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb file1_out_compressed.txt file1_compressed_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_empty(self):  # test empty file
        huffman_encode('empty.txt', 'empty_out.txt')
        err = subprocess.call("diff -wb empty_out.txt empty_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb empty_out_compressed.txt empty_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_02_textfile(self):
        huffman_encode("file2.txt", "file2_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file2_out.txt file2_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb file2_out_compressed.txt file2_compressed_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_1repeat(self):  # tests aaaaa
        huffman_encode('5a.txt', '5a_out.txt')
        err = subprocess.call("diff -wb 5a_out.txt 5a_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb 5a_out_compressed.txt 5a_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_1space(self):
        huffman_encode('1space.txt', '1space_out.txt')
        err = subprocess.call("diff -wb 1space_out.txt 1space_soln.txt", shell=True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb 1space_out_compressed.txt 1space_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_huffman_encode_empty(self):
        with self.assertRaises(FileNotFoundError):
            huffman_encode('nofile.txt', 'file1_out.txt')

    def test_parse_header(self):
        header = "97 3 98 4 99 2"
        freq_list = parse_header(header)
        self.assertEqual(freq_list[96:101], [0, 3, 4, 2, 0])
        empty = ""
        e_freq_list = parse_header(empty)
        self.assertEqual(e_freq_list[96:101], [0, 0, 0, 0, 0])

    def test_total_header(self):
        header = "97 3 98 4 99 2"
        self.assertEqual(total(header), 9)

    def test_01a_test_file1_parse_header(self):
        f = open('file1_compressed_soln.txt', 'rb')
        header = f.readline()
        f.close()
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                    0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0]
        self.compare_freq_counts(parse_header(header), expected)

    def test_01_test_file1_decode(self):
        huffman_decode("file1_compressed_soln.txt", "file1_decoded.txt")
        err = subprocess.call("diff -wb file1.txt file1_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def test_02_test_file2_decode(self):
        huffman_decode("file2_compressed_soln.txt", "file2_decoded.txt")
        err = subprocess.call("diff -wb file2.txt file2_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def test_decode_empty(self):
        huffman_decode("empty_out_compressed.txt", "empty_decoded.txt")
        err = subprocess.call("diff -wb empty.txt empty_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def test_5a(self):
        huffman_decode("5a_out_compressed.txt", "5a_decoded.txt")
        err = subprocess.call("diff -wb 5a.txt 5a_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def test_1character(self):
        huffman_decode("1space_out_compressed.txt", "1space_decoded.txt")
        err = subprocess.call("diff -wb 1space.txt 1space_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def test_huffman_decode_empty(self):
        with self.assertRaises(FileNotFoundError):
            huffman_decode('nofile.txt', 'file1_decoded.txt')

    def test_3_textfile(self):
        huffman_decode("multiline_compressed_soln.txt", "multiline_decoded.txt")
        err = subprocess.call("diff -wb multiline.txt multiline_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def test_declaration_decode(self):
        huffman_decode("declaration_compressed_soln.txt", "declaration_decoded.txt")
        err = subprocess.call("diff -wb declaration.txt declaration_decoded.txt", shell=True)
        self.assertEqual(err, 0)

    def compare_freq_counts(self, freq, exp):
        for i in range(256):
            stu = 'Frequency for ASCII ' + str(i) + ': ' + str(freq[i])
            ins = 'Frequency for ASCII ' + str(i) + ': ' + str(exp[i])
            self.assertEqual(stu, ins)


if __name__ == '__main__':
    unittest.main()

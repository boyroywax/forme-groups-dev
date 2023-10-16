import unittest
import sys
import random
import uuid

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")
# from src.groups.utils.crypto import MerkleTree
from src.groups.utils.merkle_tree_speed import MerkleTree


class TestMerkleTree(unittest.TestCase):
    def test_init(self):
        mt = MerkleTree()
        self.assertEqual(mt.root(), None)
        self.assertEqual(mt.leaves, ())

    def test_hash_single_value(self):
        hash_test_func = MerkleTree._hash_func("test")
        self.assertEqual(hash_test_func, "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")

    def test_hash_items_not_identical(self):
        hash_test_func = MerkleTree._hash_func("test")
        hash_test_func2 = MerkleTree._hash_func("test2")
        self.assertNotEqual(hash_test_func, hash_test_func2)

    def test_hash_items_identical_single(self):
        hash_test_func = MerkleTree._hash_func("test")
        hashed_items = MerkleTree._hash_items(hash_test_func)
        self.assertEqual(hashed_items, "0839734cbb5ab81cab6474a5ea4bd6a39ac09e3a7da1dd07f35d6b827d9a2177")

    def test_hash_items_identical_two_values(self):
        hash_test_func = MerkleTree._hash_func("test")
        hashed_items = MerkleTree._hash_items(hash_test_func, hash_test_func)
        self.assertEqual(hashed_items, "0839734cbb5ab81cab6474a5ea4bd6a39ac09e3a7da1dd07f35d6b827d9a2177")

    def test_hash_items_identical_using_hash_func(self):
        hash_test_func = MerkleTree._hash_func("test")
        hashed_items = MerkleTree._hash_func(hash_test_func + hash_test_func)
        self.assertEqual(hashed_items, "0839734cbb5ab81cab6474a5ea4bd6a39ac09e3a7da1dd07f35d6b827d9a2177")
    
    def test_hash_level(self):
        hash_test_func = MerkleTree._hash_func("test")
        hash_test_func2 = MerkleTree._hash_func("test2")
        hashed_items = MerkleTree._hash_items(hash_test_func, hash_test_func2)
        hashed_level = MerkleTree.hash_level((hash_test_func, hash_test_func2))
        self.assertEqual(hashed_level, (hashed_items, ))

    def test_hash_level_odd(self):
        hash_test_func = MerkleTree._hash_func("test")
        hash_test_func2 = MerkleTree._hash_func("test2")
        hash_test_func3 = MerkleTree._hash_func("test3")
        hashed_items_part1 = MerkleTree._hash_items(hash_test_func, hash_test_func2)
        print(f'hashed item part 1: {hashed_items_part1}')
        hashed_items_part2 = MerkleTree._hash_items(hash_test_func3)
        print(f'hashed item part 2: {hashed_items_part2}')
        hashed_items = MerkleTree._hash_items(hashed_items_part1, hashed_items_part2)
        print(f'hashed items: {hashed_items}')
        hashed_level = MerkleTree.hash_level((hash_test_func, hash_test_func2, hash_test_func3))
        print(f'hashed level: {hashed_level}')
        self.assertEqual(hashed_level, (hashed_items_part1, hashed_items_part2))

    def test_hash_level_even(self):
        hash_test_func = MerkleTree._hash_func("test")
        hash_test_func2 = MerkleTree._hash_func("test2")
        hash_test_func3 = MerkleTree._hash_func("test3")
        hash_test_func4 = MerkleTree._hash_func("test4")
        hashed_items_part1 = MerkleTree._hash_items(hash_test_func, hash_test_func2)
        hashed_items_part2 = MerkleTree._hash_items(hash_test_func3, hash_test_func4)
        hashed_items = MerkleTree._hash_items(hashed_items_part1, hashed_items_part2)
        hashed_level = MerkleTree.hash_level((hash_test_func, hash_test_func2, hash_test_func3, hash_test_func4))
        self.assertEqual(hashed_level, (hashed_items_part1, hashed_items_part2))

    def test_hash_level_odd_2(self):
        hash_test_func = MerkleTree._hash_func("test")
        hash_test_func2 = MerkleTree._hash_func("test2")
        hash_test_func3 = MerkleTree._hash_func("test3")
        hash_test_func4 = MerkleTree._hash_func("test4")
        hash_test_func5 = MerkleTree._hash_func("test5")
        hashed_items_part1 = MerkleTree._hash_items(hash_test_func, hash_test_func2)
        hashed_items_part2 = MerkleTree._hash_items(hash_test_func3, hash_test_func4)
        hashed_items_part3 = MerkleTree._hash_items(hash_test_func5)
        hashed_items = MerkleTree._hash_items(hashed_items_part1, hashed_items_part2)
        hashed_level = MerkleTree.hash_level((hash_test_func, hash_test_func2, hash_test_func3, hash_test_func4, hash_test_func5))
        self.assertEqual(hashed_level, (hashed_items_part1, hashed_items_part2, hashed_items_part3))

    def test_hash_build(self):
        hash_test_func = MerkleTree._hash_func("test")
        hash_test_func2 = MerkleTree._hash_func("test2")
        hashed_items = MerkleTree._hash_items(hash_test_func, hash_test_func2)
        mt = MerkleTree((hash_test_func, hash_test_func2))
        self.assertEqual(mt.root(), hashed_items)
   
    def test_hash_items_not_identical(self):
        hash_test_func = MerkleTree._hash_func("test")
        hash_test_func2 = MerkleTree._hash_func("test2")
        mt = MerkleTree((hash_test_func, hash_test_func2))
        self.assertEqual(mt.root(), '694299f8eb01a328732fb21f4163fbfaa8f60d5662f04f52ad33bec63953ec7f')

    def test_hash_items_identical_single2(self):
        hash_test_func = MerkleTree._hash_func("test")
        mt = MerkleTree((hash_test_func,))
        self.assertEqual(mt.root(), '0839734cbb5ab81cab6474a5ea4bd6a39ac09e3a7da1dd07f35d6b827d9a2177')

    def test_hash_items_identical_two_values2(self):
        hash_test_func = MerkleTree._hash_func("test")
        mt = MerkleTree((hash_test_func, hash_test_func))
        self.assertEqual(mt.root(), '0839734cbb5ab81cab6474a5ea4bd6a39ac09e3a7da1dd07f35d6b827d9a2177')

    
    def test_hash_items_with_wrong_data_type(self):
        hash_test_func = MerkleTree._hash_func("test")
        with self.assertRaises(TypeError):
            mt = MerkleTree((hash_test_func, 1))

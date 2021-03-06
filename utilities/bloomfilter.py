import mmh3
import math
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size=0, fp=0.05):
        self.fp = fp
        self.size = self.get_size(size, self.fp)
        self.hash_count = self.get_hash_count(self.size, self.fp)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def insert(self, element):
        if self.size == 0:
            return
        digests = []
        for i in range(self.hash_count):
            digest = mmh3.hash(element, i) % self.size
            digests.append(digest)
            self.bit_array[digest] = True

    def search(self, element):
        if self.size == 0:
            return False
        for i in range(self.hash_count):
            digest = mmh3.hash(element, i) % self.size
            if not self.bit_array[digest]:
                return False
        return True

    @classmethod
    def get_size(cls, n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(cls, m, n):
        k = (m / n) * math.log(2)
        return int(k)

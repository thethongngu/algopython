from math import floor, log2

class SparseTable:
    def __init__(self, arr, f):
        self.n = len(arr)
        self.k = floor(log2(self.n))
        self.f = f

        self.log_table = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log_table[i] = self.log_table[i // 2] + 1

        self.st = [([-1] * self.n) for _ in range(self.k + 1)]
        for j in range(self.n):
            self.st[0][j] = arr[j]

        for i in range(1, self.k + 1):
            j = 0
            while j + (1 << i) - 1 < self.n:
                self.st[i][j] = f(self.st[i - 1][j], self.st[i - 1][j + (1 << (i - 1))])
                j += 1

    def query(self, l, r):
        if l < 0 or r >= self.n or l > r:
            raise IndexError("Query out of range")

        i = self.log_table[r - l + 1]
        return self.f(self.st[i][l], self.st[i][r - (1 << i) + 1])

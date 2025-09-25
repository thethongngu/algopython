"""
Tested:
    - https://leetcode.com/problems/range-sum-query-immutable
    - https://leetcode.com/problems/range-sum-query-mutable
"""


class SegmentTree:
    def __init__(self, data, merge_func, identity_element):
        self.n = len(data)
        if self.n == 0:
            return

        self.data = data
        self.merge_func = merge_func
        self.identity_element = identity_element

        self.tree = [self.identity_element] * (self.n * 4)
        self._build(1, 0, self.n - 1)

    def query(self, left, right):
        if not (0 <= left <= right < self.n):
            raise IndexError("Invalid query range")
        return self._query(1, 0, self.n - 1, left, right)

    def single_update(self, index, value):
        if not (0 <= index < self.n):
            raise IndexError("Invalid update index")

        self._update(1, 0, self.n - 1, index, index, value)

    def _build(self, node, start, end):
        if start == end:
            self.tree[node] = self.data[start]
            return

        mid = (start + end) // 2
        self._build(node * 2, start, mid)
        self._build(node * 2 + 1, mid + 1, end)

        self.tree[node] = self.merge_func(self.tree[node * 2], self.tree[node * 2 + 1])

    def _update(self, node, start, end, left, right, value):
        if right < start or end < left:
            return

        if start == end:
            self.tree[node] = value
            return

        mid = (start + end) // 2
        self._update(node * 2, start, mid, left, right, value)
        self._update(node * 2 + 1, mid + 1, end, left, right, value)

        self.tree[node] = self.merge_func(self.tree[node * 2], self.tree[node * 2 + 1])

    def _query(self, node, start, end, left, right):
        if right < start or end < left:
            return self.identity_element

        if left <= start and end <= right:
            return self.tree[node]

        mid = (start + end) // 2
        return self.merge_func(
            self._query(node * 2, start, mid, left, right),
            self._query(node * 2 + 1, mid + 1, end, left, right),
        )

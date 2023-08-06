import numpy as np
from collections import deque

"""
ReplayMemory class gives an ability to store and give back data in random batches.
Memory has a limited buffer based on the FIFO queue.
"""


class ReplayMemory:
    def __init__(self, capacity=10000):
        self._capacity = capacity
        self._buffer = deque()

    def sample_batch(self, batch_size):
        """
        Creates an iterator that returns random batches from the buffer.
        The batch size has to be smaller than the current number of data elements.
        :param batch_size: batch size
        :return: iterator returning random batches
        """
        if batch_size <= 0:
            return
        ofs = 0
        vals = list(self._buffer)
        np.random.shuffle(vals)
        while (ofs + 1) * batch_size <= len(self._buffer):
            yield vals[ofs * batch_size:(ofs + 1) * batch_size]
            ofs += 1

    def append_memory(self, data):
        """
        Adds new data element to the replay memory buffer.
        When the capacity is reached, the oldest element in the
        buffer is removed.
        :param data: data element to add
        :return:
        """
        self._buffer.append(data)
        while len(self._buffer) > self._capacity:
            self._buffer.popleft()

    def is_buffer_full(self):
        """
        Tells if buffer reached the maximum value of the capacity.
        :return: True when the number of elements is equal of higher than the capacity.
        False otherwise.
        """
        return len(self._buffer) >= self._capacity

    def is_buffer_fulled_by_percentage_value(self, capacity_percantage=100):
        """
        Tells if buffer reached the given percentage of the capacity.
        The percentage value should be between 0 and 100.
        Negative values treat as 0% and value higher than 100 as 100%.
        :param capacity_percantage: the percentage of value of the buffer that we want to compare the capacity.
        :return: True when the elements in the buffer are equal or higher than
        the percentage value of the memory capacity, False otherwise.
        """
        percentage = capacity_percantage
        if percentage > 100:
            percentage = 100
        elif percentage < 0:
            percentage = 0
        return len(self._buffer) >= self._capacity * (percentage / 100.0)

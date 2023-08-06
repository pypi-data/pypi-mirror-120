from katie.rl.replay_memory import ReplayMemory
import pytest


def test_replay_memory_creation():
    default_capacity = 10000
    rm = ReplayMemory()
    assert (default_capacity == rm._capacity)


def test_replay_memory_creation_with_custom_capacity():
    for capacity in range(10, 2000, 100):
        rm = ReplayMemory(capacity=capacity)
        assert (capacity == rm._capacity)


def test_replay_memory_batch_sampling():
    capacity = 15000
    batch_size = 200
    rm = ReplayMemory(capacity=capacity)
    for n in range(0, capacity):
        rm.append_memory(n)
    expected_number_of_iterations = capacity / batch_size
    iteration = 0
    for batch in rm.sample_batch(batch_size):
        iteration += 1
    assert (expected_number_of_iterations == iteration)


def test_sample_batch_negative_batch_size():
    batch_size = -50
    rm = ReplayMemory()
    for n in range(0, rm._capacity):
        rm.append_memory(n)
    expected_number_of_iterations = 0
    iteration = 0
    for batch in rm.sample_batch(batch_size):
        iteration += 1
    assert (expected_number_of_iterations == iteration)


def test_sample_batch_zeo_batch_size():
    batch_size = 0
    rm = ReplayMemory()
    for n in range(0, rm._capacity):
        rm.append_memory(n)
    expected_number_of_iterations = 0
    iteration = 0
    for batch in rm.sample_batch(batch_size):
        iteration += 1
    assert (expected_number_of_iterations == iteration)


buffer_size_percentage_capacity_value = [
    (50, 0, True),
    (5000, 50, True),
    (4999, 50, False),
    (5001, 50, True),
    (10000, -1, True),
    (10000, 101, True),
    (0, -1, True),
    (0, 101, False),
    (9999, 100, False)
]

buffer_size_to_default_capacity_value = [
    (50, False),
    (5000, False),
    (0, False),
    (10000, True),
    (9999, False),
    (10001, True)
]


@pytest.mark.parametrize("buffer_size, percentage, expected_value", buffer_size_percentage_capacity_value)
def test_buffer_fulled_by_percentage_value(buffer_size, percentage, expected_value):
    rm = ReplayMemory()
    for n in range(0, buffer_size):
        rm.append_memory(n)
    assert (expected_value == rm.is_buffer_fulled_by_percentage_value(capacity_percantage=percentage))


@pytest.mark.parametrize("buffer_size, expected_value", buffer_size_to_default_capacity_value)
def test_buffer_fulled_by_percentage_value(buffer_size, expected_value):
    rm = ReplayMemory()
    for n in range(0, buffer_size):
        rm.append_memory(n)
    assert (expected_value == rm.is_buffer_full())

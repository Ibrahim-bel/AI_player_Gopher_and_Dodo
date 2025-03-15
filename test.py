import sys
import enum
import math
import random
import timeit
import typing
import dataclasses
import collections
from collections import namedtuple

repeat = 5
number = 1000
N = 5000

# Define the different Point structures
PointTuple = namedtuple('PointTuple', ['x', 'y', 'z'])

from dataclasses import dataclass

@dataclass
class PointDataclass:
    x: int
    y: int
    z: int

@dataclass(slots=True)
class PointDataclassSlots:
    x: int
    y: int
    z: int

class PointObject:
    __slots__ = ['x', 'y', 'z']
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class PointEnum(enum.Enum):
    x = 1234
    y = 5678
    z = 9012
    def __call__(self, value):
        return value

# Define the tests
def test_namedtuple_attr():
    point = PointTuple(1234, 5678, 9012)
    for i in range(N):
        x, y, z = point.x, point.y, point.z

def test_namedtuple_index():
    point = PointTuple(1234, 5678, 9012)
    for i in range(N):
        x, y, z = point

def test_namedtuple_unpack():
    point = PointTuple(1234, 5678, 9012)
    for i in range(N):
        x, *y = point

def test_dataclass():
    point = PointDataclass(1234, 5678, 9012)
    for i in range(N):
        x, y, z = point.x, point.y, point.z

def test_dataclass_slots():
    point = PointDataclassSlots(1234, 5678, 9012)
    for i in range(N):
        x, y, z = point.x, point.y, point.z

def test_dict():
    point = dict(x=1234, y=5678, z=9012)
    for i in range(N):
        x, y, z = point['x'], point['y'], point['z']

def test_slots():
    point = PointObject(1234, 5678, 9012)
    for i in range(N):
        x, y, z = point.x, point.y, point.z

def test_enum_attr():
    point = PointEnum
    for i in range(N):
        x, y, z = point.x, point.y, point.z

def test_enum_call():
    point = PointEnum
    for i in range(N):
        x, y, z = point.x.value, point.y.value, point.z.value

def test_enum_item():
    point = PointEnum
    for i in range(N):
        x, y, z = point['x'], point['y'], point['z']

# Run the benchmarks
if __name__ == '__main__':
    tests = [
        test_namedtuple_attr,
        test_namedtuple_index,
        test_namedtuple_unpack,
        test_dataclass,
        test_dataclass_slots,
        test_dict,
        test_slots,
        test_enum_attr,
        test_enum_call,
        test_enum_item,
    ]

    print(f'Running tests {repeat} times with {number} calls.')
    print(f'Using {N} iterations in the loop')

    results = collections.defaultdict(lambda: math.inf)

    for i in range(repeat):
        # Shuffling tests to prevent skewed results due to CPU boosting or thermal throttling
        random.shuffle(tests)

        print(f'Run {i}:', end=' ')
        for t in tests:
            name = t.__name__

            print(name, end=', ')
            sys.stdout.flush()

            timer = timeit.Timer(f'{name}()', f'from __main__ import {name}')
            results[name] = min(results[name], timer.timeit(number))

        print()

    for name, result in sorted(results.items(), key=lambda x: x[::-1]):
        print(f'{name:30} {result:.3f}s')


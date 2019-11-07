import math
import random


def generate_matrix(m: int, il: int) -> list:
    matrix_n_m = []
    for i in range(il):
        matrix_n_m.append([random.choice([0, 1]) for _ in range(m)])
    return matrix_n_m


def bin_to_dec(arr: list) -> int:
    out = []
    for i in range(len(arr)):
        curr_index = len(arr) - i - 1
        curr_item = arr[curr_index]
        out.append(curr_item * pow(2, curr_index))
    return sum(out)


def find_m(a: int, b: int, d: int) -> int:
    volume_size = (b - a) * pow(10, d)
    m = 0
    while not (volume_size <= pow(2, m)):
        m += 1
    return m


def normalize_x(x: int, a: int, b: int, m: int) -> float:
    return a + (b - a) * x / (pow(2, m) - 1)


def rastrigin(arr: list) -> float:
    a = 10
    w = 20 * math.pi
    return a * len(arr) + sum([pow(x, 2) - a * math.cos(w * x) for x in arr])

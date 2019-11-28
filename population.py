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


class Population:
    def __init__(self, n_dimension: int, a: int, b: int, d: int, il: int, arr_n: list):
        self.n_dimension = n_dimension
        self.a = a
        self.b = b
        self.d = d
        self.il = il
        self.arr_n = arr_n

    def generate_population(self) -> list:
        final_array = []
        final_matrix = []
        for i in range(self.n_dimension):
            try:
                _a = self.arr_n[i]["a"] if self.arr_n[i]["a"] is not None else self.a
                _b = self.arr_n[i]["b"] if self.arr_n[i]["b"] is not None else self.b
                _d = self.arr_n[i]["d"] if self.arr_n[i]["d"] is not None else self.d

                m = find_m(_a, _b, _d)

                self.arr_n[i].update({"a": _a, "b": _b, "d": _d, "m": m})

            except IndexError:
                m = find_m(self.a, self.b, self.d)
                self.arr_n.append({"m": m, "a": self.a, "b": self.b, "d": self.d})

        self.arr_n = self.arr_n[:self.n_dimension]

        for i, curr_arr in enumerate(self.arr_n):
            generated_matrix = generate_matrix(curr_arr["m"], self.il)
            final_matrix.append(generated_matrix)

        for i, curr_arr in enumerate(final_matrix):
            for index, item in enumerate(curr_arr):
                if index >= len(final_array):
                    final_array.append({})
                chromosomes = final_array[index].get("chromosomes", [])
                chromosome = {**self.arr_n[i], "gens": item}

                chromosomes.append(chromosome)
                final_array[index]["chromosomes"] = chromosomes
        return final_array

    @staticmethod
    def calc_match(population):
        for p in population:
            chromosomes = p["chromosomes"]
            gens = [chromosome["gens"] for chromosome in chromosomes]
            gens = [bin_to_dec(g) for g in gens]
            gens = [
                normalize_x(item, chromosomes[index]["a"], chromosomes[index]["b"], chromosomes[index]["m"])
                for index, item in enumerate(gens)
            ]

            p["eval"] = rastrigin(gens)
        return population

from utils import generate_matrix, bin_to_dec, find_m, normalize_x, rastrigin


class Population:
    def __init__(self, n_dimension: int, a: int, b: int, d: int, il: int, arr_n: list):
        self.n_dimension = n_dimension
        self.a = a
        self.b = b
        self.d = d
        self.il = il
        self.arr_n = arr_n

    def generate_population(self) -> list:
        sum_m = 0
        final_array = []
        final_matrix = []
        for i in range(self.n_dimension):
            try:
                _a = self.arr_n[i]["a"] if self.arr_n[i]["a"] is not None else self.a
                _b = self.arr_n[i]["b"] if self.arr_n[i]["b"] is not None else self.b
                _d = self.arr_n[i]["d"] if self.arr_n[i]["d"] is not None else self.d

                m = find_m(_a, _b, _d)

                self.arr_n[i].update({"a": _a, "b": _b, "d": _d, "m": m})

                sum_m += m
            except IndexError:
                m = find_m(self.a, self.b, self.d)
                sum_m += m
                self.arr_n.append({"m": m, "a": self.a, "b": self.b, "d": self.d})

        self.arr_n = self.arr_n[:self.n_dimension]

        for i, curr_arr in enumerate(self.arr_n):
            generated_matrix = generate_matrix(curr_arr["m"], self.il)
            final_matrix.append(generated_matrix)

            converted_bin_to_dec = [bin_to_dec(a) for a in generated_matrix]
            normalized_array = [
                normalize_x(x, curr_arr["a"], curr_arr["b"], curr_arr["m"])
                for x in converted_bin_to_dec
            ]

            for index, item in enumerate(normalized_array):
                if index < len(final_array):
                    final_array[index].append(item)
                else:
                    final_array.append([item])
        final_array = [{"eval": rastrigin(a)} for a in final_array]

        for i, curr_arr in enumerate(final_matrix):
            for index, item in enumerate(curr_arr):
                chromosomes = final_array[index].get("chromosomes", [])
                chromosome = {**self.arr_n[i], "gens": item}

                chromosomes.append(chromosome)
                final_array[index]["chromosomes"] = chromosomes
        return final_array

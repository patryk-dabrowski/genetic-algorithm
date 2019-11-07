from utils import generate_matrix, bin_to_dec, find_m, normalize_x, rastrigin
from methods import SelectMethod, RankingMethod, TournamentMethod


def main():
    n_dimension = 3
    d = 6
    a = -1
    b = 1
    il = 10

    arr_n = [
        {"a": -1, "b": 1, "d": 6},
        {"a": -2, "b": 2, "d": 7},
        {"a": -3, "b": 0, "d": 3},
    ]

    population = generate_population(n_dimension, a, b, d, il, arr_n)
    select_max = SelectMethod(population=population, is_min=False)
    ranking_max = RankingMethod(population=population, is_min=False)
    ranking_min = RankingMethod(population=population, is_min=True)
    tournament_without_return_max = TournamentMethod(population=population, is_min=False, without_return=True)
    tournament_without_return_min = TournamentMethod(population=population, is_min=True, without_return=True)
    tournament_with_return_max = TournamentMethod(population=population, is_min=False, without_return=False)
    tournament_with_return_min = TournamentMethod(population=population, is_min=True, without_return=False)

    # Debug section
    print("Metoda selekcji MAX", select_max.calc())
    print("Metoda rankingowa MAX", ranking_max.calc())
    print("Metoda rankingowa MIN", ranking_min.calc())
    print("Metoda turniejowa bez zwracania MAX", tournament_without_return_max.calc())
    print("Metoda turniejowa bez zwracania MIN", tournament_without_return_min.calc())
    print("Metoda turniejowa zwracania MAX", tournament_with_return_max.calc())
    print("Metoda turniejowa zwracania MIN", tournament_with_return_min.calc())


def generate_population(
    n_dimension: int, a: int, b: int, d: int, il: int, arr_n: list
) -> list:
    sum_m = 0
    final_array = []
    for i in range(n_dimension):
        try:
            _a = arr_n[i]["a"] if arr_n[i]["a"] is not None else a
            _b = arr_n[i]["b"] if arr_n[i]["b"] is not None else b
            _d = arr_n[i]["d"] if arr_n[i]["d"] is not None else d

            m = find_m(_a, _b, _d)

            arr_n[i].update({"a": _a, "b": _b, "d": _d, "m": m})

            sum_m += m
        except IndexError:
            m = find_m(a, b, d)
            sum_m += m
            arr_n.append({"m": m, "a": a, "b": b, "d": d})

    arr_n = arr_n[:n_dimension]

    for i, curr_arr in enumerate(arr_n):
        generated_matrix = generate_matrix(curr_arr["m"], il)

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

        # print(f"Matrix {i}: a = {curr_arr['a']}; b = {curr_arr['b']}; d = {curr_arr['d']}; m = {curr_arr['m']}")
        # [print(row, b2d, norm) for row, b2d, norm in zip(generated_matrix, converted_bin_to_dec, normalized_array)]
        # print()
    # print("List of x; result of rastrigin function")
    # [print(a, "f(x)=", r) for a, r in zip(final_array, [rastrigin(a) for a in final_array])]
    return [rastrigin(a) for a in final_array]


if __name__ == "__main__":
    main()

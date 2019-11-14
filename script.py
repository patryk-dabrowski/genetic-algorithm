from population import Population


def debug_population(population):
    for p in population:
        print([chromosome["gens"] for chromosome in p["chromosomes"]])


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

    population = (Population(n_dimension, a, b, d, il, arr_n)).generate_population()

    # Debug section
    print("Population", population)
    debug_population(population)
    print()


if __name__ == "__main__":
    main()

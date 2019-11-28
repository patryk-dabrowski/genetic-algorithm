from operators import Mutation, Inversion, KPointCrossover, UniformCrossover
from population import Population
from selects import RouletteMethod


def debug_population(population) -> None:
    for p in population:
        print([chromosome["gens"] for chromosome in p["chromosomes"]])


def main():
    n_dimension = 3
    d = 6
    a = -1
    b = 1
    il = 10

    options = {
        "arr_n": [
            {"a": -1, "b": 1, "d": 6},
            {"a": -2, "b": 2, "d": 7},
            {"a": -3, "b": 0, "d": 3},
        ],
        "select_method": RouletteMethod,
        "select_options": {
            "is_min": False,
            "without_return": False
        },
        "operators": [
            Mutation,
            Inversion,
            KPointCrossover,
            UniformCrossover
        ],
        "operators_options": {
            "k": None
        }
    }

    # Generate population
    population = (Population(n_dimension, a, b, d, il, options["arr_n"])).generate_population()
    # Calculate match
    population = Population.calc_match(population)

    # Select children
    select_method = options.get("select_method", RouletteMethod)
    select_options = options.get("select_options", {})
    select = select_method(population, **select_options)
    population = select.execute()

    # Genetic operators
    children = []
    for operator in options.get("operators", []):
        operator_options = options.get("operator_options", {})
        instance = operator(population, **operator_options)
        executed = instance.execute()
        children += executed

    # Succession

    # [print(p) for p in population]


if __name__ == "__main__":
    main()

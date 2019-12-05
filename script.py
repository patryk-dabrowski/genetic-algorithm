from operators import Mutation, Inversion, KPointCrossover, UniformCrossover
from population import Population
from selects import RouletteMethod, RankingMethod
from succession import TriviaSuccession, PartialSuccession, EliteSuccession, RandomSuccession, CompressionSuccession


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
        "is_min": False,
        "select_method": RankingMethod,
        "select_options": {
            "without_return": False
        },
        "operators": [
            Mutation,
            Inversion,
            UniformCrossover
        ],
        "operators_options": {
            "k": None
        },
        # "succession": TriviaSuccession,
        # "succession": PartialSuccession,
        # "succession": EliteSuccession,
        # "succession": CompressionSuccession,
        "succession": RandomSuccession,
    }

    # Generate population
    population = (Population(n_dimension, a, b, d, il, options["arr_n"])).generate_population()
    # Calculate match
    population = Population.calc_match(population)

    is_min = options.get("is_min", False)

    for epoch in range(1000):
        # print("Epoch:", epoch)
        # Select children
        select_method = options.get("select_method", RouletteMethod)
        select_options = options.get("select_options", {})
        select = select_method(population, is_min, **select_options)
        selected_population = select.execute()

        # Genetic operators
        children = []
        for operator in options.get("operators", []):
            operator_options = options.get("operator_options", {})
            operator_instance = operator(selected_population, **operator_options)
            executed = operator_instance.execute()
            executed = Population.calc_match(executed)
            children += executed

        # Succession
        succession = options.get("succession", TriviaSuccession)
        succession_instance = succession(parents=population, children=children, is_min=is_min)
        population = succession_instance.execute()

    [print(p) for p in population]


if __name__ == "__main__":
    main()

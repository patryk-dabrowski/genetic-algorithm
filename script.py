from methods import RouletteMethod, RankingMethod, TournamentMethod
from population import Population


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

    roulette_max = RouletteMethod(population=population, is_min=False)
    roulette_min = RouletteMethod(population=population, is_min=True)
    ranking_max = RankingMethod(population=population, is_min=False)
    ranking_min = RankingMethod(population=population, is_min=True)
    tournament_without_return_max = TournamentMethod(population=population, is_min=False, without_return=True)
    tournament_without_return_min = TournamentMethod(population=population, is_min=True, without_return=True)
    tournament_with_return_max = TournamentMethod(population=population, is_min=False, without_return=False)
    tournament_with_return_min = TournamentMethod(population=population, is_min=True, without_return=False)

    # Debug section
    print("Population", population)


if __name__ == "__main__":
    main()

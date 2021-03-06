import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import spacegame
import multiprocessing.dummy as mp
from more_itertools import chunked
import fire
from functools import partial

POOLSIZE = 100
pool = mp.Pool(POOLSIZE)


def linearpolicy(obsv, particle):
    return particle @ obsv


def objectivefn(particles, render=False):
    particles = [particles]
    rewards = []
    for pchunks in list(chunked(particles, POOLSIZE)):
        orgs = list(map(lambda x: x.reshape(2, 8), pchunks))
        r = pool.map(
            lambda o: spacegame.play(policy=linearpolicy, organism=o, render=render),
            orgs,
        )
        rewards += r

    return -np.array(rewards)







def main(POPSIZE, GENS, RENDER):

    varbound = np.array([[-50, 50]] * 16)

    algorithm_param = {
        "max_num_iteration": GENS,
        "population_size": POPSIZE,
        "mutation_probability": 0.1,
        "elit_ratio": 0,
        "crossover_probability": 0.5,
        "parents_portion": 0.3,
        "crossover_type": "uniform",
        "max_iteration_without_improv": None,
    }

    model = ga(
        function=partial(objectivefn, render=RENDER),
        dimension=16,
        variable_type="real",
        variable_boundaries=varbound,
        algorithm_parameters=algorithm_param,
    )

    x = model.run()
    print("----")
    best_org = model.best_variable
    spacegame.play(
        policy=linearpolicy, organism=np.array(best_org).reshape(2, 8), render=True
    )

if __name__ == "__main__":
    fire.Fire(main)

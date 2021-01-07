#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from simulation import Simulation
import random

def main():
    population_seller = 100
    population_buyer = 100
    average_degree = 4          # Average degree of social network
    num_episode = 5             # Number of total episode in a single simulation for taking ensemble average
    #lamda = 0.6					# sellerの費率

    simulation = Simulation(population_seller, population_buyer, average_degree)

    for episode in range(num_episode):
        random.seed()
        simulation.one_episode(episode)

if __name__ == '__main__':
    main()

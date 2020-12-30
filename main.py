#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from simulation import Simulation
import random

def main():
    population_seller = 50
    population_buyer = 50
    average_degree_seller = 8          # Average degree of social network
    average_degree_buyer = 8          # Average degree of social network
    num_episode = 1             # Number of total episode in a single simulation for taking ensemble average
    #lamda = 0.6					# sellerの費率

    simulation = Simulation(population_seller, population_buyer, average_degree_seller, average_degree_buyer)

    for episode in range(num_episode):
        random.seed()
        simulation.one_episode(episode)

if __name__ == '__main__':
    main()

import numpy as np
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from seller import Seller
from buyer import Buyer

class Simulation(Buyer, Seller):
    
    def __init__(self, population_seller, population_buyer,average_degree_seller, average_degree_buyer):
        self.sellers = self.__generate_sellers(population_seller, population_buyer, average_degree_seller)
        self.initial_honest_sellers = self.__choose_initial_honest_sellers()

        self.buyers = self.__generate_buyers(population_seller, population_buyer, average_degree_buyer)
        self.initial_simple_buyers = self.__choose_initial_simple_buyers()
        super().__init__()

    def __generate_sellers(self, population_seller, population_buyer, average_degree_seller):
        rearange_edges = int(average_degree_seller*0.5)
        self.network_seller = nx.barabasi_albert_graph(population_buyer, rearange_edges)#sellerの取引相手のnodeなのでbuyer
        #num_sellers = int(population_seller)

        sellers = [Seller() for id in range(population_seller)]#rangeで0~populationまでの数字をAgentに割り付ける
        for index, focal_seller in enumerate(sellers):#enumerateでforループの中のリストやタプルにインデックス番号をつける
            next_sellers_id = list(self.network_seller[index])
            for nb_id in next_sellers_id:
                focal_seller.next_sellers_id.append(nb_id)#appendで末尾に要素を追加
        
        return sellers

    def __generate_buyers(self, population_seller, population_buyer, average_degree_buyer):
        rearange_edges = int(average_degree_buyer*0.5)
        self.network_buyer = nx.barabasi_albert_graph(population_seller, rearange_edges)#buyerの取引相手のnodeなのでseller
        #num_buyers = int(population_buyer)

        buyers = [Buyer() for id in range(population_buyer)]#rangeで0~populationまでの数字をAgentに割り付ける
        for index, focal_buyer in enumerate(buyers):#enumerateでforループの中のリストやタプルにインデックス番号をつける
            next_buyers_id = list(self.network_buyer[index])
            for nb_id in next_buyers_id:
                focal_buyer.next_buyers_id.append(nb_id)#appendで末尾に要素を追加
        return buyers

    def __choose_initial_honest_sellers(self):
        population = len(self.sellers)
        self.initial_honest_sellers = rnd.sample(range(population), k = int(population/2))


    def __choose_initial_simple_buyers(self):
        population = len(self.buyers)
        self.initial_simple_buyers = rnd.sample(range(population), k = int(population/2))

    def __initialize_strategy_sellers(self):
        """Initialize the strategy of agents"""
        for index, focal_seller in enumerate(self.sellers):
            if index in self.initial_honest_sellers:
                focal_seller.strategy = "H"
            else:
                focal_seller.strategy = "L"

    def __initialize_strategy_buyers(self):
        """Initialize the strategy of agents"""
        for index, focal_buyer in enumerate(self.buyers):
            if index in self.initial_simple_buyers:
                focal_buyer.strategy = "Buy"
            else:
                focal_buyer.strategy = "NotBuy"

    def __count_payoff_seller(self):
        """Count the payoff based on payoff matrix"""
        for focal_seller in self.sellers:
            focal_seller.point = 0.0
            for nb_id in focal_seller.neighbors_id:
                neighbor = self.sellers[nb_id]
                if focal_seller.strategy == "L" and neighbor.strategy == "Buy":    
                    focal_seller.point += Dg
                elif focal_seller.strategy == "L" and neighbor.strategy == "NotBuy":   
                    focal_seller.point += -1/self.asset_price
                elif focal_seller.strategy == "H" and neighbor.strategy == "Buy":   
                    focal_seller.point += 0
                elif focal_seller.strategy == "H" and neighbor.strategy == "NotBuy":  
                    focal_seller.point += -1/self.asset_price
    
    def __count_payoff_buyer(self):
        """Count the payoff based on payoff matrix"""
        for focal_buyer in self.buyers:
            focal_buyer.point = 0.0
            for nb_id in focal_buyer.neighbors_id:
                neighbor = self.buyers[nb_id]
                if focal_buyer.strategy == "Buy" and neighbor.strategy == "L":    
                    focal_buyer.point += -Dg
                elif focal_buyer.strategy == "NotBuy" and neighbor.strategy == "L":   
                    focal_buyer.point += -1/neighbor.asset_price
                elif focal_buyer.strategy == "Buy" and neighbor.strategy == "H":   
                    focal_buyer.point += 0
                elif focal_buyer.strategy == "NotBuy" and neighbor.strategy == "H":  
                    focal_buyer.point += -1/neighbor.asset_price


    def __update_strategy_seller(self):
        for focal_seller in self.sellers:
            focal_seller.decide_next_strategy(self.sellers)
        
        for focal_seller in self.sellers:
            focal_seller.update_strategy()

    def __update_strategy_buyer(self):
        for focal_buyer in self.buyers:
            focal_buyer.decide_next_strategy(self.buyers)
        
        for focal_buyer in self.buyers:
            focal_buyer.update_strategy()

    def __count_fc_seller(self):
        """Calculate the fraction of cooperative agents"""
        
        fc_seller = len([seller for seller in self.sellers if seller.strategy == "H"])/len(self.sellers)
    
        return fc_seller

    def __count_fc_buyer(self):
        """Calculate the fraction of cooperative agents"""
        
        fc_buyer = len([buyer for buyer in self.buyers if buyer.strategy == "Buy"])/len(self.buyers)
    
        return fc_buyer

    def __play_game(self, episode, Dg):
        """Continue games until fc gets converged"""
        tmax = 3000

        self.__initialize_strategy_sellers()
        initial_fc_seller = self.__count_fc_seller()
        fc_hist_seller = [initial_fc_seller]
        

        self.__initialize_strategy_buyers()
        initial_fc_buyer = self.__count_fc_buyer()
        fc_hist_buyer = [initial_fc_buyer]


        print(f"Episode:{episode}, Dg:{Dg:.1f}, Time: 0, Fc_S:{initial_fc_seller:.3f}, Fc_B:{initial_fc_buyer:.3f}")
        # result = pd.DataFrame({'Time': [0], 'Fc': [initial_fc]})

        for t in range(1, tmax+1):
            self.__count_payoff_seller(Dg)
            self.__update_strategy_seller()
            self.__update_strategy_buyer()
            fc_s = self.__count_fc_seller()
            fc_hist_seller.append(fc_s)
            print(f"Episode:{episode}, Dg:{Dg:.1f}, Time:{t}, Fc_S:{fc_s:.3f}")
            # new_result = pd.DataFrame([[t, fc]], columns = ['Time', 'Fc'])
            # result = result.append(new_result)

            # Convergence conditions
            if fc == 0 or fc == 1:
                fc_converged = fc
                comment = "Fc(0 or 1"
                break

            if t >= 100 and np.absolute(np.mean(fc_hist_seller[t-100:t-1]) - fc)/fc < 0.001:
                fc_converged = np.mean(fc_hist_seller[t-99:t])
                comment = "Fc(converged)"
                break

            if t == tmax:
                fc_converged = np.mean(fc_hist_seller[t-99:t])
                comment = "Fc(final timestep)"
                break

        print(f"Dg:{Dg:.1f}, Time:{t}, {comment}:{fc_converged:.3f}")
        # result.to_csv(f"time_evolution_Dg_{Dg:.1f}_Dr_{Dr:.1f}.csv")

        return fc_converged

    def __take_snapshot(self, timestep):
        for index, focal_seller in enumerate(self.sellers):
                if focal_seller.strategy == "H":
                    self.network.nodes[index]["strategy"] = "H"
                else:
                    self.network.nodes[index]["strategy"] = "L"

        def color(i):
            if self.network.nodes[i]["strategy"] == "H":
                return 'cyan'
            else:
                return 'pink'
            
        color =  dict((i, color(i)) for i in self.network.nodes())
        pos = nx.spring_layout(self.network)
                
        nx.draw_networkx_edges(self.network, pos)
        nx.draw_networkx_nodes(self.network, pos, node_color = list(color.values()), node_size = 10)
        plt.title('t={}'.format(timestep), fontsize=20)
        plt.xticks([])
        plt.yticks([])
        plt.savefig(f"snapshot_t={timestep}.png")
        plt.close()

    def one_episode(self, episode):
        """Run one episode"""

        result = pd.DataFrame({'Dg': [], 'Fc_S': []})
        self.__choose_initial_honest_sellers()

        for Dg in np.arange(0, 1.1, 0.1):
            fc_converged = self.__play_game(episode, Dg)
            new_result = pd.DataFrame([[format(Dg, '.1f'), fc_converged]], columns = ['Dg', 'Fc_S'])
            result = result.append(new_result)
        
        result.to_csv(f"phase_diagram{episode}.csv")

# print(Simulation.__mro__)
# s = Simulation(100,100,4)
# print(s.__play_game)
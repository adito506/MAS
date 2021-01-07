import numpy as np
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from seller import Seller
from buyer import Buyer

class Simulation(Seller):
    
    def __init__(self, population_seller, population_buyer, average_degree):
        self.seller = self.__generate_seller(population_seller, population_buyer, average_degree)
        self.initial_honest_seller = self.__choose_initial_honest_seller()
        self.buyer = self.__generate_buyer(population_seller, population_buyer, average_degree)
        self.initial_simple_buyer = self.__choose_initial_simple_buyer()
        

    def __generate_seller(self, population_seller, population_buyer, average_degree):
        rearange_edges = int(average_degree)
        self.network_seller = nx.barabasi_albert_graph(population_buyer, rearange_edges)#sellerの取引相手のnodeなのでbuyer
        self.network_opponent = nx.barabasi_albert_graph(population_seller, rearange_edges)#得点を比較する相手
        
        seller = [Seller() for id in range(population_seller)]#rangeで0~populationまでの数字をAgentに割り付ける
        for index, focal_seller in enumerate(seller):#enumerateでforループの中のリストやタプルにインデックス番号をつける
            next_buyer_id = list(self.network_seller[index])
            opponent_id = list(self.network_opponent[index])
            for nb_id in next_buyer_id:
                focal_seller.next_buyer_id.append(nb_id)#appendで末尾に要素を追加
                for opp_id in opponent_id:
                    focal_seller.opponent_id.append(opp_id)
        return seller

    def __generate_buyer(self, population_seller, population_buyer, average_degree):
        rearange_edges = int(average_degree)
        self.network_buyer = nx.barabasi_albert_graph(population_seller, rearange_edges)#buyerの取引相手のnodeなのでseller
        self.network_opponent = nx.barabasi_albert_graph(population_buyer, rearange_edges)#得点を比較する相手

        buyer = [Buyer() for id in range(population_buyer)]#rangeで0~populationまでの数字をAgentに割り付ける
        for index, focal_buyer in enumerate(buyer):#enumerateでforループの中のリストやタプルにインデックス番号をつける
            next_seller_id = list(self.network_buyer[index])
            opponent_id = list(self.network_opponent[index])
            for nb_id in next_seller_id:
                focal_buyer.next_seller_id.append(nb_id)#appendで末尾に要素を追加
                for opp_id in opponent_id:
                    focal_buyer.opponent_id.append(opp_id)
        return buyer

    def __choose_initial_honest_seller(self):
        population = len(self.seller)
        initial_honest_seller = rnd.sample(range(population), k = int(population/2))
        return initial_honest_seller


    def __choose_initial_simple_buyer(self):
        population = len(self.buyer)
        initial_simple_buyer = rnd.sample(range(population), k = int(population/2))
        return initial_simple_buyer
        #元のコードではself.initial_simple_buyerと定義していたが、Noneになるため、書き方を変えた

    def __initialize_strategy_seller(self):
        """Initialize the strategy of agents"""
        for index, focal_seller in enumerate(self.seller):
            if index in self.initial_honest_seller:
                focal_seller.strategy = "H"
            else:
                focal_seller.strategy = "L"

    def __initialize_strategy_buyer(self):
        """Initialize the strategy of agents"""
        for index, focal_buyer in enumerate(self.buyer):
            if index in self.initial_simple_buyer:
                focal_buyer.strategy = "Buy"
            else:
                focal_buyer.strategy = "NotBuy"
                #self.buyerがnoneになっている

    def __count_payoff_seller(self, Pr, r, h_q):
        """利得表に基づいて売主が獲得する利得を計算"""
        R = 0
        S = -r*h_q
        T = h_q*Pr
        P = -r*h_q

        for focal_seller in self.seller:
            focal_seller.point = 0.0
            for nb_id in focal_seller.next_buyer_id:
                neighbor = self.seller[nb_id]
                if focal_seller.strategy == "L" and neighbor.strategy == "Buy":    
                    focal_seller.point += T
                elif focal_seller.strategy == "L" and neighbor.strategy == "NotBuy":   
                    focal_seller.point += P
                elif focal_seller.strategy == "H" and neighbor.strategy == "Buy":   
                    focal_seller.point += R
                elif focal_seller.strategy == "H" and neighbor.strategy == "NotBuy":  
                    focal_seller.point += S
    
    def __count_payoff_buyer(self, Pr, r, h_q):
        """利得表に基づいて買主が獲得する利得を計算"""
        R = 0
        S = -r*h_q
        T = -h_q*Pr
        P = -r*h_q

        for focal_buyer in self.buyer:
            focal_buyer.point = 0.0
            for nb_id in focal_buyer.next_seller_id:
                neighbor = self.buyer[nb_id]
                if focal_buyer.strategy == "Buy" and neighbor.strategy == "L":    
                    focal_buyer.point += T
                elif focal_buyer.strategy == "NotBuy" and neighbor.strategy == "L":   
                    focal_buyer.point += P
                elif focal_buyer.strategy == "Buy" and neighbor.strategy == "H":   
                    focal_buyer.point += R
                elif focal_buyer.strategy == "NotBuy" and neighbor.strategy == "H":  
                    focal_buyer.point += S


    def __update_strategy_seller(self):
        for focal_seller in self.seller:
            focal_seller.decide_next_strategy(self.seller)
        
        for focal_seller in self.seller:
            focal_seller.update_strategy()

    def __update_strategy_buyer(self):
        for focal_buyer in self.buyer:
            focal_buyer.decide_next_strategy(self.buyer)
        
        for focal_buyer in self.buyer:
            focal_buyer.update_strategy()

    def __count_fc_seller(self):
        """Calculate the fraction of cooperative agents"""
        
        fc_seller = len([seller for seller in self.seller if seller.strategy == "H"])/len(self.seller)
    
        return fc_seller

    def __count_fc_buyer(self):
        """Calculate the fraction of cooperative agents"""
        
        fc_buyer = len([buyer for buyer in self.buyer if buyer.strategy == "Buy"])/len(self.buyer)
    
        return fc_buyer

    def __house_quality(self):
        h_q = 100
        return h_q

    def __play_game(self, episode, Pr, r, h_q):
        """Continue games until fc gets converged"""
        tmax = 3000

        self.__initialize_strategy_seller()
        initial_fc_seller = self.__count_fc_seller()
        fc_hist_seller = [initial_fc_seller]
        

        self.__initialize_strategy_buyer()
        initial_fc_buyer = self.__count_fc_buyer()
        fc_hist_buyer = [initial_fc_buyer]


        print(f"Episode:{episode}, Time: 0, Pr:{Pr:.1f}, r:{r:.2f}, Fc_S:{initial_fc_seller:.3f}, Fc_B:{initial_fc_buyer:.3f}")
        # result = pd.DataFrame({'Time': [0], 'Fc': [initial_fc]})

        for t in range(1, tmax+1):
            self.__count_payoff_seller(Pr, r, h_q)
            self.__update_strategy_seller()
            fc_s = self.__count_fc_seller()
            fc_hist_seller.append(fc_s)
            self.__count_payoff_buyer(Pr, r, h_q)
            self.__update_strategy_buyer()
            fc_b = self.__count_fc_buyer()
            fc_hist_buyer.append(fc_b)
            print(f"Episode:{episode}, Time:{t}, Pr:{Pr:.1f}, r:{r:.2f}, Fc_S:{fc_s:.3f}, Fc_B:{fc_b:.3f}")
            # new_result = pd.DataFrame([[t, fc]], columns = ['Time', 'Fc'])
            # result = result.append(new_result)

            # Convergence conditions
            if fc_s == 0 or fc_s == 1 or fc_b == 0 or fc_b == 1:
                fc_converged = fc_s
                fc_sold = fc_b
                comment = "Fc_S(0 or 1"
                break

            if t >= 100 and np.absolute(np.mean(fc_hist_seller[t-100:t-1]) - fc_s)/fc_s < 0.001:
                fc_converged = np.mean(fc_hist_seller[t-99:t])
                fc_sold = np.mean(fc_hist_buyer[t-99:t])
                comment = "Fc_S(converged)"
                break

            if t >= 100 and np.absolute(np.mean(fc_hist_buyer[t-100:t-1]) - fc_b)/fc_b < 0.001:
                fc_converged = np.mean(fc_hist_seller[t-99:t])
                fc_sold = np.mean(fc_hist_buyer[t-99:t])
                comment = "Fc_B(converged)"
                break

            if t == tmax:
                fc_converged = np.mean(fc_hist_seller[t-99:t])
                fc_sold = np.mean(fc_hist_buyer[t-99:t])
                comment = "Fc(final timestep)"
                break

        print(f"Pr:{Pr:.1f}, r:{r:.1f}, Time:{t}, {comment}:{fc_converged:.3f}:{fc_sold:.3f}")
        return fc_converged, fc_sold

    def __take_snapshot(self, timestep):
        for index, focal_seller in enumerate(self.seller):
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
        """全パラメータ領域でplay_gameを実行し、計算結果をCSVに書き出す"""

        result = pd.DataFrame({'Pr': [], 'r': [], 'Fc_S': [], 'Fc_B': []})
        self.__choose_initial_honest_seller()
        self.__choose_initial_simple_buyer()

        for Pr in np.arange(0, 1.1, 0.1):
            for r in np.arange(0.01, 0.11, 0.01):
                h_q = self.__house_quality()
                fc_converged = self.__play_game(episode, Pr, r, h_q)
                new_result = pd.DataFrame([[format(Pr, '.1f'), format(r, '.2f'), fc_converged[0],fc_converged[1]]], columns = ['Pr', 'r', 'Fc_S', 'Fc_B'])
                result = result.append(new_result)
        
        result.to_csv(f"phase_diagram{episode}.csv")

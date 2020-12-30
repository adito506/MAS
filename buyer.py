import random as rnd
import numpy as np

class Buyer:    
    def __init__(self):
        self.point = 0.0
        self.strategy = None
        self.next_strategy = None
        self.next_buyers_id = []
        super().__init__() #Simulation classで多重継承しているので、強制的にinitする処理を記載

        
    def decide_next_strategy(self, buyers):
        opp_id_buyer = rnd.choice(self.next_buyers_id)   # Choose opponent from neighbors
        opp_buyer = buyers[opp_id_buyer]

        if opp_buyer.strategy != self.strategy and rnd.random() < 1/(1 + np.exp((self.point - opp_buyer.point)/0.1)):
            self.next_strategy = opp_buyer.strategy
        else:
            self.next_strategy = self.strategy

    def update_strategy(self):
        self.strategy = self.next_strategy

# byr = Buyer()
# print(byr)
import random as rnd
import numpy as np

class Seller:
    
    def __init__(self):
        # self.asset_price = 0.0
        self.point = 0.0
        self.strategy = None
        self.next_strategy = None
        self.opponent_id = []
        self.next_buyer_id = []
        super().__init__()

        
    def decide_next_strategy(self, seller):
        opp_id = rnd.choice(self.next_buyer_id)   # Choose opponent from neighbors
        opp = seller[opp_id]

        if opp.strategy != self.strategy and rnd.random() < 1/(1 + np.exp((self.point - opp.point)/0.1)):
            self.next_strategy = opp.strategy
        else:
            self.next_strategy = self.strategy

    def update_strategy(self):
        self.strategy = self.next_strategy

    # def decide_asset_price(self):
    #     self.asset_price = rnd.randint(50,100)
    #保有している資産価格をランダムに決める

    #def decide_profit(self):
    #    self.profit = rnd.randint(1,20)
    #取引時に上乗せする利鞘をランダムに決める

# sll = Seller()
# print(sll)
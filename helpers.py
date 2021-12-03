from itertools import count
import pickle
from _pickle import load

class Item:
    _ids = count(0)
    def __init__(self, name, model, buyPrice, buyDate):
        self.name = name
        self.model = model
        self.buyPrice = buyPrice
        self.buyDate = buyDate
        self.id = next(self._ids)
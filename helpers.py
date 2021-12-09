from itertools import count
import pickle

class Item:
    _ids = count(0)
    def __init__(self, name, model, buyPrice, buyDate):
        self.name = name
        self.model = model
        self.buyPrice = buyPrice
        self.buyDate = buyDate
        self.id = next(self._ids)

    def getName(self):
        return str(self.name)

####              Transaction Class              ####
#
#   type: sale or purchase
#   item: Item object
#   buyer: name of the purchaser
#   market: Facebook Marketplace, Reddit, eBay, Other
#   saleDate: Tuple of when the item was sold
#   val: final amount recieved from sale
#
#####################################################

class Transaction:
    _its = count(0)
    def __init__(self, type, item, buyer, market, saleDate, val):
        self.type = type
        self.item = item
        self.buyer = buyer
        self.market = market
        self.saleDate = saleDate
        self.val = val

    def transPrint(self):
        print(self.item.getName() + " was sold to " + self.buyer + " on " +
        str(self.saleDate) + " thru " + self.market + " for a total of " + str(self.val))

from classes import *

#Global Variables
accountBalance = 0
salesTotal = 0
typesOfInventory = ["GBASP", "GBA", "GBC", "N64"]
inventory = []
cont = True

#Putting in some fake gameboys
for i in range(10):
    gbasp = Item(r"0" + str(i), i, 80, (11, 23, 21))
    inventory.append(("GBASP", gbasp))

## Menu Options ##

#Returns the current inventory count of each type of item
def listInventory(val):
    type = typesOfInventory[val]
    count = 0

    #Count the number of items of type typesOfInventory[val]
    for item in inventory:
        if item[0] == type:
            count += 1
    print(type + ": " + str(count))

    #Try to count the next type of inventory, if it exists
    try:
        if typesOfInventory[val+1] != None:
            listInventory(val+1)
    except:
        print("End of Inventory")

#Adds an item to inventory and subtracts the price from the account balance
def buyItem(val):
    #Create a new item
    global accountBalance
    print(typesOfInventory)
    type = input("Enter the item type... ")
    item = Item(input("Enter the item name... "),
     input("Enter the item model... "),
      int(input("Enter the item price... ")),
       tuple(input("Input the purchase date in the following format (month, day, year)... ")))

    #Add it to the inventory list
    inventory.append((type.upper(), item))

    #Subtract the items costs from the standing account balance
    accountBalance -= item.buyPrice

#Removes an item from the inventory and addes the sale price to the sales total and account balance
def sellItem(val):
    global salesTotal
    global accountBalance
    tempList = []
    print(typesOfInventory)
    #Pick a type of inventory to sell
    type = input("What type of item did you sell? ").upper()

    #Print all the items in that inventory
    for item in inventory:
        if item[0] == type:
            print(str(item[1].id) + ": " + str(item[1].name) + ", $" + str(item[1].buyPrice))
            tempList.append(int(item[1].id))
    #Select an ID to sell
    if len(tempList) > 0:
        id = int(input("Which item did you sell? Type the item ID... "))
    else:
        print("No items of that type found")
        return

    #Making sure that the item selected is on the screen
    for currID in tempList:
        if id == currID:
            #Remove the item from the inventory
            for item in inventory:
                if id == int(item[1].id):
                    inventory.remove(item)

            #Add the sale price to the sales total and the account balance
            price = int(input("How much did you recieve on the sale? "))
            salesTotal += price
            accountBalance += price
            return
    print("Item not found")


#Adds an item to inventory but does not affect the account balance
def addItem(val):
    #Create a new item
    global accountBalance
    print(typesOfInventory)
    type = input("Enter the item type... ")
    item = Item(input("Enter the item name... "),
     input("Enter the item model... "),
      int(input("Enter the item price... ")),
       tuple(input("Input the purchase date in the following format (month, day, year)... ")))

    #Add it to the inventory list
    inventory.append((type.upper(), item))

#Removes an item from the inventory without affecting the sales total or account balance
def removeItem(val):
    print(typesOfInventory)
    #Pick a type of inventory to sell
    type = input("What type of item did you want to remove? ").upper()

    #Print all the items in that inventory
    for item in inventory:
        if item[0] == type:
            print(str(item[1].id) + ": " + str(item[1].name) + ", $" + str(item[1].buyPrice))

    #Select an ID to sell
    id = int(input("Which item did you want to remove? Type the item ID... "))

    #Remove the item from the inventory
    for item in inventory:
        if id == int(item[1].id):
            inventory.remove(item)

#Gets the account balance and sales revenue
def getAccountBalance(val):
    print("Account Balance: $" + str(accountBalance))
    print("Sales Revenue: $" + str(salesTotal))

#Ends the program
def endProgram(val):
    global cont
    cont = False

menuOptions = {
    "LIST INVENTORY" : listInventory,
    "BUY ITEM": buyItem,
    "SELL ITEM": sellItem,
    "ADD ITEM": addItem,
    "REMOVE ITEM": removeItem,
    "ACCOUNT BALANCE": getAccountBalance,
    "EXIT": endProgram
    }

while cont:
    print(list(menuOptions.keys()))

    menuOptions[input("Enter menu option... ").upper()](0)

print("Program Execution Complete")

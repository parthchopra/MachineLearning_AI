import numpy as np 
import pandas as pd

def createItem(dataSet):
    
    itemList = []
    
    for transaction in dataSet:
        for item in transaction:
            if not [item] in itemList:
                
                 # creating unique single lists in Itemlist. ie list of all items
                itemList.append([item])
                
    itemList.sort()
    
    return list(map(frozenset, itemList))


def scanData(data, itemsetk, minSupport):
    
    tempDict = {}
    
    for transaction in data:
        for item in itemsetk:
            if item.issubset(transaction):
                if not item in tempDict: 
                    tempDict[item]=1 # tempDict contains number of all items
                else: 
                    tempDict[item] += 1
    
    numItems = float(len(data))
    freqItemset = []
    supportDict = {}
    
    for key in tempDict:
        support = tempDict[key]/numItems 
        
        if support >= minSupport:
            freqItemset.insert(0,key) # freqItemset contains all frequent items
        supportDict[key] = support # contains support of all items
    
    return freqItemset, supportDict


def itemSetGenerator(itemsetk, k):
 
    higherOrderitemset = []
    lenitemsetk = len(itemsetk)
    
    
    for i in range(lenitemsetk):
        for j in range(i+1, lenitemsetk): 
            L1 = list(itemsetk[i])[:k-2] 
            L2 = list(itemsetk[j])[:k-2]
            L1.sort() 
            L2.sort()
            
            # Two frequent itemsets of order k are merged only if their k-1 itemsets are identical
            if L1 == L2:
                higherOrderitemset.append(itemsetk[i] | itemsetk[j]) # Performing set union creates itemset with n+1 items
               
    return higherOrderitemset

def apriori(dataSet, minSupport):
    
    itemList = createItem(dataSet) # Creating frozenset of items
    
    
    # Generating all the frequent 1-itemsets and the support of those items
    freqItemset1, supportDict = scanData(dataSet, itemList, minSupport)
    freqItemsets = [freqItemset1]
    k = 2 
    
    while (len(freqItemsets[k-2]) > 0): # Incrementing k until we no longer find any kth order itemsets
        
        itemsetk = itemSetGenerator(freqItemsets[k-2], k) # Generating itemsets of order k
        
        # Generating the frequent itemset for the kth order and support for each of these itemsets
        freqItemsetk, supportDictk = scanData(dataSet, itemsetk, minSupport) 
        
        supportDict.update(supportDictk)
        freqItemsets.append(freqItemsetk)
        
        k += 1
    return freqItemsets, supportDict




Market_Data = pd.read_csv('Market_Basket_Optimisation.csv',index_col=None, header = None ) # Use your local path here

dataSet = []

for index, transaction in Market_Data.iterrows():
    cleaned_transaction = transaction[~transaction.isnull()].tolist()
    dataSet.append(cleaned_transaction)

freqItemsets, supportDict = apriori(dataSet, minSupport = 0.001)
f = freqItemsets
s = supportDict
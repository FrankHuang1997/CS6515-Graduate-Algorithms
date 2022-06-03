# -*- coding: utf-8 -*-

"""

knapsack.py - CS6515, Intro to Graduate Algorithms

Implement a Dynamic Programming Solution to the knapsack problem.   The program will be given a
dictionary of items and an overall weight limit.  It should select the combination of items 
which achieves the highest value without exceeding the weight limit.    

NOTE:  Each item may be selected at most one time (non-repeating).

About the Input:

	itemsDict -- a dictionary of items, where the key is an integer 1...N (inclusive),
	             and the value is a tuple (name, weight, value) where:

			     name is the text name of the item
				 weight is the item weight
				 value is the item value

	maxWt -- the maximum weight supported by the knapsack

	There is at least one item available
	All weights and values are >0
	All test cases will have a solution (at least one item can be inserted in the knapsack)

"""
import argparse  # argparse allows the parsing of command line arguments
import GA_ProjectUtils as util  # utility functions for cs 6515 projects


def initTable(numItems, maxWt):
    """
    Initialize the table to be used to record the best value possible for given
    item idx and weight
    NOTE : this table must:
              -- be 2 dimensional (i.e. T[x][y])
              -- contain a single numeric value (no tuples or other complicated abstract data types)
    """
    # TODO Replace the following with your code to initialize the table properly

    T = [[0 for j in range(0, maxWt+1)] for i in range(0, numItems + 1)]
    return T


def buildItemIter(numItems):
    """
    Build item iterator - iterator through all available items
        numItems : number of items

    Note: the index (key value) for items are integer values 1..N
    """
    # TODO Replace the following with your code to build the item iterator

    return range(1, numItems + 1)


def buildWeightIter(maxWt):
    """
    Build weight iterator - iterator of all possible integer weight values
        maxWt : maximum weight available
    """
    # TODO Replace the following with your code to build the weight iterator

    return range(1, maxWt+1)


def subProblem(T, weight, itemIDX, itemWt, itemVal):
    """
    Define the subproblem to solve for each table entry - set the value to be maximum for a given
    item and weight value
        T : the table being populated
        weight : weight from iteration through possible weight values
        itemIDX : the index (key value) of the item from the loop iteration
        itemWt : the weight of the item
        itemVal : the value of the item
    """
    # TODO Replace the following with your code to solve the subproblem appropriately!

    if itemWt > weight:
        T[itemIDX][weight] = T[itemIDX - 1][weight]
    else:
        T[itemIDX][weight] = max(itemVal + T[itemIDX - 1][weight - itemWt], T[itemIDX - 1][weight])

    return T[itemIDX][weight]


def buildResultList(T, itemsDict, maxWt):
    """
    Construct list of items that should be chosen.
        T : the populated table of item values, indexed by item idx and weight
        itemsDict : dictionary of items   Note: items are indexed 1..N
        maxWt : maximum weight allowed

    	result: a list composed of item tuples
    """
    result = []

    # TODO Your code goes here to build the list of chosen items!
    w = maxWt
    for i in range(len(itemsDict), 0, -1):
        if T[i][w] <= 0:
            break
        if T[i][w] == T[i - 1][w]:
            continue
        else:
            result.append(itemsDict[i])
            w = w - itemsDict[i][1]
    return result


def knapsack(itemsDict, maxWt):
    """
    Solve the knapsack problem for the passed list of items and max allowable weight
    DO NOT MODIFY THE FOLLOWING FUNCTION
    NOTE : There are many ways to solve this problem.  You are to solve it
            using a 2D table, by filling in the function templates above.
            If not directed, do not modify the given code template.
    """
    numItems = len(itemsDict)
    # initialize table properly
    table = initTable(numItems, maxWt)
    # build iterables
    # item iterator
    itemIter = buildItemIter(numItems)
    # weight iterator
    weightIter = buildWeightIter(maxWt)

    for itmIdx in itemIter:
        # query item values from list
        item, itemWt, itemVal = itemsDict[itmIdx]
        for w in weightIter:
            # expand table values by solving subproblem
            table[itmIdx][w] = subProblem(table, w, itmIdx, itemWt, itemVal)

    # build list of results - chosen items to maximize value for a given weight
    return buildResultList(table, itemsDict, maxWt)


def main():
    """
    The main function
    """
    # DO NOT REMOVE ANY ARGUMENTS FROM THE ARGPARSER BELOW
    # You may change default values, but any values you set will be overridden when autograded
    parser = argparse.ArgumentParser(description='Knapsack Coding Quiz')
    parser.add_argument('-i', '--items', help='File holding list of possible Items (name, wt, value)',
                        default='defaultItems.txt', dest='itemsListFileName')
    parser.add_argument('-w', '--weight', help='Maximum (integer) weight of items allowed', type=int, default=200,
                        dest='maxWeight')

    # args for autograder, DO NOT MODIFY ANY OF THESE
    parser.add_argument('-n', '--sName', help='Student name, used for autograder', default='GT', dest='studentName')
    parser.add_argument('-a', '--autograde', help='Autograder-called (2) or not (1=default)', type=int, choices=[1, 2],
                        default=1, dest='autograde')
    args = parser.parse_args()

    # DO NOT MODIFY ANY OF THE FOLLOWING CODE
    itemsDict = util.buildKnapsackItemsDict(args)
    itemsChosen = knapsack(itemsDict, args.maxWeight)
    util.displayKnapSack(args, itemsChosen)


if __name__ == '__main__':
    main()

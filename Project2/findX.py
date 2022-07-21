# -*- coding: utf-8 -*-

"""

findX.py - Intro to Graduate Algorithms

Solve the findX in an Infinite array problem using a Divide & Conquer method
Your runtime must be O(log n)

The array of values is indexed A[1..n] inclusive

Your code MUST NOT directly reference any variables in findX.  The following methods are available:
    
    findX.start(seed) -- returns the value (x) to search for within the array
    findX.lookup(i) -- returns A[i] or None if i>n
    findX.lookups() -- returns the number of calls to lookup

""" 
#argparse allows the parsing of command line arguments
import argparse
#utility functions for cs 6515 projects
import GA_ProjectUtils as util


def findXinA(x, findX):

    #TODO Your Code Begins Here, DO NOT MODIFY ANY CODE ABOVE THIS LINE
    high_index = 1
    a_high = findX.lookup(high_index)
    while(a_high < x and a_high is not None):
        high_index = high_index * 2
        a_high = findX.lookup(high_index)
        if a_high is None:
            break
    low_index = high_index//2
    if high_index == 1:
        value = findX.lookup(1)
        if value is None:
            theIndex = None
        elif value == x:
            theIndex = 1
        else:
            theIndex = None

    else:
        def binary_search(low, high, v):
            if low <= high:
                mid = (high + low)//2
                a_mid = findX.lookup(mid)
                if a_mid is None:
                    return binary_search(low, mid-1, v)
                else:
                    if a_mid == v:
                        return mid
                    elif a_mid > x:
                        return binary_search(low, mid-1, v)
                    else:
                        return binary_search(mid+1, high, v)
            else:
                return None


        theIndex = binary_search(low_index, high_index, x)

    #TODOne Your code Ends here, DO NOT MOIDFY ANYTHING BELOW THIS LINE

    numLookups = findX.lookups()

    return theIndex, numLookups


def main():
    """
    main - DO NOT CHANGE ANYTHING BELOW THIS LINE
    """
    # DO NOT REMOVE ANY ARGUMENTS FROM THE ARGPARSER BELOW
    parser = argparse.ArgumentParser(description='Find X Coding Quiz')

    #args for autograder, DO NOT MODIFY ANY OF THESE
    parser.add_argument('-a', '--autograde',  help='Autograder-called (2) or not (1=default)', type=int, choices=[1, 2], default=1, dest='autograde')
    parser.add_argument('-s', '--seed', help='seed value for random function', type=int, default=123456, dest='seed')
    parser.add_argument('-l', '--nLower', help='lower bound for N', type=int, default=10, dest='nLower')
    parser.add_argument('-u', '--nUpper', help='upper bound for N', type=int, default=100000, dest='nUpper')

    args = parser.parse_args()

    #DO NOT MODIFY ANY OF THE FOLLOWING CODE

    findX = util.findX()
    x = findX.start(args.seed, args.nLower, args.nUpper)
    index, calls = findXinA(x, findX)
    print('findX result: x found at index {} in {} calls'.format(index, calls))

    return

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Utility functions - do not modify these functions!  Some of these functions may not be applicable to your project.  Ignore them

If you find errors post to class piazza page.

"""
#import time
#import os
#useful structure to build dictionaries of lists
#from collections import defaultdict

########################################
#IO and Util functions  

#returns sorted version of l, and idx order of sort
def getSortResIDXs(l, rev=True):
    from operator import itemgetter  
    return list(zip(*sorted([(i,e) for i,e in enumerate(l)], 
                        key=itemgetter(1),reverse=rev)))


#read srcFile into list of ints 
def readIntFileDat(srcFile):
    strs = readFileDat(srcFile)
    res = [int(s.strip()) for s in strs]
    return res

#read srcFile into list of floats 
def readFloatFileDat(srcFile):
    strs = readFileDat(srcFile)
    res = [float(s.strip()) for s in strs]
    return res

#read srcFile into list of strings
def readFileDat(srcFile):
    import os
    try:
        f = open(srcFile, 'r')
    except IOError:
        #file doesn't exist, return empty list
        print(('Note : {} does not exist in current dir : {}'.format(srcFile, os.getcwd())))
        return []
    src_lines = f.readlines()
    f.close()
    return src_lines

#write datList into fName file
def writeFileDat(fName, datList):
    f = open(fName, 'w')
    for item in datList:
        print(item, file=f)
    f.close()
    
#append record to existing file
def appendFileDat(fName, dat):
    f = open(fName, 'a+')
    print(dat, file=f)
    f.close()
    
    
#######################################
#Homework mini-project utility functions

##Knapsack

#this will build a default dictionary of items, where the key is the item number (1..n)
#and value is tuple of (name, item weight, value)

def buildKnapsackItemsDict(args):
    ksItemsData = readFileDat(args.itemsListFileName)
    items = {}
    itemCount = 0
    for line in ksItemsData:
        itemCount += 1
        vals = line.split(',')
        tupleVal = (vals[0].strip(), int(vals[1].strip()), int(vals[2].strip()))
        items[itemCount] = tupleVal
        
#    lst = sorted(res, key = lambda x: x[0])

    if args.autograde == 1:
        print("The following items were loaded from file {} : \nName, Integer Weight, Integer Value : ".format(args.itemsListFileName))
        for k, val in items.items():
            print("{0:30} Wt : {1:5} Val : {2:5} ".format(val[0],val[1],val[2]))

    return items

#Will display results of knapsack problem
def displayKnapSack(args, itemsChosen):
    if(len(itemsChosen)!=0):      
        print("\n\nResults : The following items were chosen : ") 
        lst = sorted(itemsChosen, key = lambda x: x[0])
        ttlWt = 0
        ttlVal = 0
        for s in lst:
            ttlWt += s[1]
            ttlVal += s[2]
            print("{0:30} Wt : {1:5} Val : {2:5} ".format(s[0],s[1],s[2]))
      
        print(("For a total value of <%i> and a total weight of [%i]" % (ttlVal, ttlWt)))
    else : 
        print("\n\nResults : No Items were chosen: ") 

##End Knapsack

##MST
#this function will load graph information from file and build the graph structure
def build_MSTBaseGraph(args):
    #file format should be
    #line 0 : # of verts
    #line 1 : # of edges
    #line 2... : vert1 vert2 edgeWT
    MSTGraphData = readFileDat(args.graphDataFileName)
    numVerts = int(MSTGraphData[0].strip())
    numEdges = int(MSTGraphData[1].strip())
    edgeDataAra = []
    for i in range(numEdges):
        line = MSTGraphData[i+2]
        vals = line.split()
        v1 = int(vals[0].strip())
        v2 = int(vals[1].strip())
        wt = float(vals[2].strip())
        #print("v1 :{} v2 :{} wt : {} ".format(v1,v2,wt))
        edgeDataAra.append([wt,v1,v2])

    G = Graph(numVerts, edgeDataAra)
    return G

def print_MSTResults(MST):
    itr = 0
    for E in MST:
        print("({:4d},{:4d}) {:2.6f} ".format(E[1][0], E[1][1], E[0]), end=" | ")
        itr += 1
        if(itr > 2):
            itr=0
            print("")
    print("\n")

"""
    build a tuple holding edge weight and edge verts to add to mst
"""
def buildMSTEdge(G, e):
    wt = G.edgeWts[e]
    return (wt, e)


def save_MSTRes(args, MST):
    saveName = "soln_"+args.graphDataFileName
    strList = []
    for E in MST:
        strDat = "{} {} {}".format(E[1][0],E[1][1],E[0])
        strList.append(strDat)
    writeFileDat(saveName, strList)


def load_MSTRes(args):
    solnName = "soln_"+args.graphDataFileName
    resDataList = readFileDat(solnName)

    MST = set()
    for line in resDataList :
        vals = line.split()
        v1 = int(vals[0].strip())
        v2 = int(vals[1].strip())
        wt = float(vals[2].strip())

        MST.add((wt, (v1,v2)))
    return MST

#u
def findTotalWeightOfMst(MST):
    totWt = 0
    for E in MST:
        totWt += E[0]

    return totWt

#used locally
def _compareTwoMSTs(MST_1, lbl1, MST_2, lbl2, printMST):
    wt1 = round(findTotalWeightOfMst(MST_1), 12)
    wt2 = round(findTotalWeightOfMst(MST_2), 12)
    if(abs(wt1 - wt2) < 1e-12):
        print("Correct: {} Weight : {} {} Wt : {} ".format(lbl1, wt1, lbl2, wt2))
        return True
    else:
        diff12 = MST_1 - MST_2
        sizeDiff12 =  len(diff12)
        diff21 = MST_2 - MST_1
        sizeDiff21 =  len(diff21)
        print("Incorrect: {} Weight : {} {} Wt : {}".format(lbl1, wt1, lbl2, wt2))
        return False


"""
    verifies results of kruskal calculation
"""
def verify_MSTKruskalResults(args, MST_Kruskal, printMST=False):
    MST_Correct = load_MSTRes(args)

    if(printMST):
        if(len(MST_Kruskal) < 1):
            print("No Kruskal's Algorithm results found (Empty MST)")
        else :
            print("Kruskal's Algorithm results (Edge list of MST) : ")
            print_MSTResults(MST_Kruskal)
        print("\n")
        print("Correct results : ")
        print_MSTResults(MST_Correct)
        print("\n")

    return _compareTwoMSTs(MST_Kruskal,"Kruskal's Result", MST_Correct, "Expected Result", printMST)


"""
    this structure will represent an undirected graph as an adjacency matrix
"""
class Graph:
    def __init__(self, numVerts, edgeDataAra):
        self.numVerts = numVerts
        self.numEdges = len(edgeDataAra)
        self.edgeDataAra = edgeDataAra

        self.edges = set()
        self.edgeWts = dict()

        # populate the graph
        for edge in edgeDataAra:
            #add edge so that lowest vert is always first
            if(edge[1] > edge[2]):
                thisEdge = (edge[2],edge[1])
            else :
                thisEdge = (edge[1],edge[2])

            self.edges.add(thisEdge)
            self.edgeWts[thisEdge] = edge[0]

    """
        returns list of edges sorted in increasing weight
    """
    def sortedEdges(self):
        sortedEdges = sorted(self.edges, key=lambda e:self.edgeWts[e])
        return sortedEdges

    def buildAdjacencyMat(self):
        numVerts = self.numVerts
        graphAdjMat = [[0]*numVerts for _ in range(numVerts)]
        edgeDataAra = self.edgeDataAra
        for edge in edgeDataAra:
            graphAdjMat[edge[1]][edge[2]] = edge[0]
            graphAdjMat[edge[2]][edge[1]] = edge[0]

        # use adjacent matrix to represent the graph
        return graphAdjMat


    """
        for debug purposes
    """
    def printMe(self):
        print("Graph has :{} vertices and {} edges".format(self.numVerts,self.numEdges))
        NumVerts = min(10, self.numVerts)

        AM = [[0.0 for _ in range(NumVerts)] for _ in range(NumVerts)]

        for edge in self.edges:
            a,b = edge
            if a > NumVerts: continue
            if b > NumVerts: continue
            weight = self.edgeWts[edge]
            AM[a][b] = weight
            AM[b][a] = weight

        print('  ', end = '  ')
        for i in range(NumVerts):
            print('{0:5d}'.format(i), end = '  ')
        print()

        for i, row in enumerate(AM):
            print('{0:2d}'.format(i), end='  ')
            for j in row:
                if j == 0:
                    print('     ', end = '  ')
                else:
                    print('{0:1.3f}'.format(j),end='  ')
            print()

        print()


##End MST

########################################
#Bloom Filter Project functions
    
#this will compare the contents of the resList with the data in baseFile
#and display performance
def compareResults(resList, configData):
    baseFileName = configData['valFileName']
    baseRes = readFileDat(baseFileName)
    if(len(baseRes) != len(resList) ):
        print('compareFiles : Failure : Attempting to compare different size lists')
        return None
    numFail = 0
    numFTrueRes = 0
    numFFalseRes = 0
    for i in range(len(resList)):
        if (resList[i].strip().lower() != baseRes[i].strip().lower()):
            resVal = resList[i].strip().lower()
            baseResVal = baseRes[i].strip().lower()
            #uncomment this to see inconsistencies
            #print('i : ' + str(i) + ': reslist : ' + resVal + ' | baseres : ' + baseResVal)
            numFail += 1
            if resVal == 'true' :
                numFTrueRes += 1
            else :
                numFFalseRes += 1
    if(numFail == 0):
        print('compareResults : Your bloom filter performs as expected')        
    else:
        print(('compareResults : Number of mismatches in bloomfilter compared to validation file : ' + str(numFail) + '| # of incorrect true results : ' + str(numFTrueRes) + '| # of incorrect False results : ' + str(numFFalseRes)))
    if((configData['studentName'] != '') and (configData['autograde'] == 2)):
        gradeRes = configData['studentName'] + ', ' + str(numFail) + ', ' + str(numFTrueRes) + ', ' + str(numFFalseRes)
        print(('saving results for ' + gradeRes + ' to autogradeResult.txt'))
        appendFileDat('autogradeResult.txt', gradeRes)
        

#this will process input configuration and return a dictionary holding the relevant info
def buildBFConfigStruct(args):
    import time
    bfConfigData = readFileDat(args.configFileName)
    configData = dict()
    for line in bfConfigData:
        #build dictionary on non-list elements
        if (line[0]=='#') or ('_' in line):
            continue
        elems = line.split('=')
        if('name' in elems[0]):
            configData[elems[0]]=elems[1].strip()
        else :
            configData[elems[0]]=int(elems[1])
    
    if ('Type 1' in configData['name']):   
        configData['type'] = 1
        configData['seeds'] = buildSeedList(bfConfigData, int(configData['k']))
        
    elif ('Type 2' in configData['name']):
        configData['type'] = 2
        aListData = []
        bListData = []
        listToAppend = aListData
        for line in bfConfigData:
            if (line[0]=='#'):
                if ('b() seeds' in line):
                    listToAppend = bListData
                continue
            listToAppend.append(line)
        
        configData['a']= buildSeedList(aListData, int(configData['k']))
        configData['b']= buildSeedList(bListData, int(configData['k']))   
    else :
        configData['type'] = -1
        print('unknown hash function specified in config file')
    
    configData['task'] = int(args.taskToDo)
    if configData['task'] != 2 :
        configData['genSeed'] =  int(time.time()*1000.0) & 0x7FFFFFFF  #(int)(tOffLong & 0x7FFFFFFF);
        print(('Random Time Seed is : ' + str(configData['genSeed'])))

    configData['inFileName'] = args.inFileName
    configData['outFileName'] = args.outFileName
    configData['configFileName'] = args.configFileName
    configData['valFileName'] = args.valFileName
    configData['studentName'] = args.studentName
    configData['autograde'] = int(args.autograde)
    
    for k,v in list(configData.items()):
        print(('Key = ' + k + ': Val = '), end=' ')
        print(v)
        
    return configData
    
def buildSeedList(stringList, k):
    res = [0 for x in range(k)]
    for line in stringList:
        if ('_' not in line) or (line[0]=='#'):
            continue
        elems = line.split('=')        
        araElems = elems[0].split('_')
        res[int(araElems[1])]=int(elems[1])
    return res


"""
    Function provided for convenience, to find next prime value from passed value
    Use this to find an appropriate prime size for type 2 hashes.
    
    Finds next prime value larger than n via brute force.  Checks subsequent numbers 
    until prime is found - should be much less than 160 checks for any values 
    seen in this project since largest gap g between two primes for any 32 bit 
    signed int is going to be g < 336, and only have to check at most every 
    other value in gap. For more, see this article : 
        https://en.wikipedia.org/wiki/Prime_gap
    
    n  : some value
    return next largest prime
"""
def findNextPrime(n):
    if (n==2) : 
        return 2
    if (n%2==0):	
        n+=1      
    #n is odd here; 336 is larger than largest gap between 2 consequtive 32 bit primes
    for i in range (n,(n + 336), 2):
        if checkIfPrime(i):
            return i            
    #error no prime found returns -1
    return -1
	
"""
    check if value is prime, return true/false
    n value to check
"""
def checkIfPrime(n):
    if (n < 2) : return False
    if (n < 4) : return True
    if ((n % 2 == 0) or (n % 3 == 0)): return False
    sqrtN = n**(.5)
    i = 5
    w = 2
    while (i <= sqrtN):
        if (n % i == 0): return False	  
        i += w
        #addresses mod2 and mod3 above, flip flops between looking ahead 2 and 4 (every other odd is divisible by 3)
        w = 6-w
    return True

## end bloom filter functions
######################################
    
########################################
#Page Rank Functions  

    
#get file values for particular object and alpha value 
#results are list of nodes, list of rank values and dictionary matching node to rank value
#list of nodes and list of rank values are sorted
def getResForPlots(prObj, alpha):
    outFileName = makeResOutFileName(prObj.inFileName, alpha, prObj.sinkHandling) 
    vNodeIDs_unsr, vRankVec_unsr = loadRankVectorData(outFileName, isTest=False)
    #build dictionary that links node id to rank value
    vNodeDict = buildValidationDict(vNodeIDs_unsr,vRankVec_unsr) 
    
    #build sorted list          
    vNodeIDs, vRankVec = getSortResIDXs(vRankVec_unsr)    
    return vNodeIDs, vRankVec, vNodeDict

#build appropriate results file name based on passed input name, alpha and sink handling flag
def makeResOutFileName(inFileName,alpha,sinkHandling):
    nameList = inFileName.strip().split('.')
    namePrefix = '.'.join(nameList[:-1])
    #build base output file name based on input file name and whether or not using selfloops to handle sinks
    outFileName = "{}_{}_{}.{}".format(namePrefix,("SL" if sinkHandling==0 else "T3"), alpha,nameList[-1])
    return outFileName     

#builds output file names given passed file name
def buildPROutFNames(fName, getVerifyNames=False):    
    #construct ouput file names based on fName (which is input file name : i.e. 'inputstuff.txt')
    nameList = fName.strip().split('.')
    #name without extension
    namePrefix = '.'.join(nameList[:-1])
    if getVerifyNames :
        #get names for verification files
        #file holding rank vector values
        voutFName = '{}-{}.{}'.format(namePrefix, 'verifyRVec',nameList[-1])
        return voutFName
    else :
        #names for saving results or accessing saved results
        #file holding rank vector values
        outFName = '{}-{}.{}'.format(namePrefix, 'outputPR',nameList[-1])
        return outFName

    
#this will build a dictionary with :
#   keys == graph nodes and 
#   values == list of pages accessible from key
#   and will also return a list of all node ids
#   using terminology from lecture, this builds the "out list" for each node in 
#   file, and a list of all node ids
def loadGraphADJList(fName):
    from collections import defaultdict
    #defaultDict has 0/empty list entry for non-present keys,  
    #does not return invalid key error
    resDict = defaultdict(list)
    filedat = readFileDat(fName)
    allNodesSet = set()
    #each line has a single number, followed by a colon, followed by a list of 
    #1 or more numbers spearated by commas
    #these represent node x : reachable nodes from node x
    for line in filedat:
        vals = line.strip().split(':')
        adjValStrs = vals[1].strip().split(',')
        #convert list of strings to list of ints           
        adjVals = [int(s.strip()) for s in adjValStrs]
        key = int(vals[0].strip())
        allNodesSet.add(key)
        allNodesSet.update(adjVals)  
        resDict[key] = adjVals  
    return resDict, list(allNodesSet)

#given the base input file name
#this will return a list of nodes in order of rank (if rankName file exists)
#and a vector of rank values as floats (if outputName file exists)
#using either base file extensions or the verification file names
def loadRankVectorData(fName, isTest=False):
    outFName = buildPROutFNames(fName, isTest)
    #read rank vector as list of floats, expected to be in order of node ids
    rankVec = readFloatFileDat(outFName)

    rankedIDS = list(range(len(rankVec)))       
    #either output, or both, might be empty list(s) if files don't exist
    return rankedIDS, rankVec   


#will save a list of nodes in order of rank, and rank values (the rank vector) for those nodes in same order
#in two separate files 
def saveRankData(fName, rankVec=None):
    outFName = buildPROutFNames(fName)

    if(rankVec != None):
        writeFileDat(outFName, rankVec)        
        print(('Rank vector saved to file {}'.format(outFName)))
        

#build a dictionary that will have node id as key and rank vector value as value - used for verification since equal rank vector values might be in different order        
def buildValidationDict(nodeIDs, rankVec):
    vDict = {}
    for x in range(len(nodeIDs)):
        vDict[nodeIDs[x]] = rankVec[x]
    return vDict
     
"""
using provided output file, verify calculated page rank is the same as expected results
args used for autograder version
"""
def verifyResults(prObj, args=None, eps=.00001): 
    print(('\nVerifying results for input file "{}" using alpha={} and {} sink handling :\n'.format(prObj.inFileName, prObj.alpha, ('self loop' if prObj.sinkHandling==0 else 'type 3'))))
    #load derived values from run of page rank
    calcNodeIDs,calcRankVec = loadRankVectorData(prObj.outFileName, isTest=False)
    #load verification data
    vNodeIDs, vRankVec = loadRankVectorData(prObj.outFileName, isTest=True)
    if (len(vNodeIDs) == 0) or (len(vRankVec)==0) :
        print ('Validation data not found, cannot test results')
        return False
    
    
    #compare nodeID order
    if(len(calcNodeIDs) != len(vNodeIDs)) :
        print(('!!!! Error : incorrect # of nodes in calculated page rank - yours has {}; validation has {}'.format(len(calcNodeIDs),len(vNodeIDs))))
        return False
    print('Calculated Rank vector is of appropriate length')
    
    #need to verify that rank vector sums to 1
    cRVecSum = sum(calcRankVec)
    if abs(cRVecSum - 1) > eps :
        print(('!!!! Error : your calculated rank vector values do not sum to 1.0 : {} '.format(cRVecSum)))
        return False
    print('Calculated Rank vector has appropriate magnitude of 1.0')
 
    #build dictionary of validation data and test data - doing this because order might be different for nodes with same rank value
    validDict = buildValidationDict(vNodeIDs,vRankVec)
    calcDict = buildValidationDict(calcNodeIDs,calcRankVec)

    
    #compare if matched - Note nodes with same rank value vector value might be out of order
    for x in range(len(vNodeIDs)):
        if abs(calcDict[vNodeIDs[x]] - validDict[vNodeIDs[x]]) > eps :
            print(('!!!! Error : rank vector values do not match, starting at idx {}, node {}, in validation node id list'.format(x,vNodeIDs[x])))
            return False
    print('Rank Vector values match verification vector values')        

    return True    

#autograder code
def autogradePR(prObj, args, prMadeTime):
    print(('Running autograder on {} for prObj with input file {}'.format(args.studentName, prObj.inFileName)))
    
 
#End Page Rank Functions
#########################################################################
# Start findXinA Functions  (Added Summer 2020 rockograziano@gatech.edu
    
import random
import math
import sys

class ExceededLookupsError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return '{0}'.format(self.message)
        else:
            return 'ExceededLookups: Program Exceeded the allowed number of lookups'


class findX():
    def __init__(self):
        self.__A = []
        self.__n = 0
        self.x = 0
        self.__lookupCount=0
        self.__maxCalls = 0
        return
    
    def start(self, seed, nLower=10, nUpper=100000):
        random.seed(seed)
        self.__lookupCount=0
        self.__n = random.randint(nLower, nUpper)
        self.__A = random.sample(range(nUpper*2), self.__n+1) # sample extra value to avoid A[n] error
        self.__A.sort()
        self.x = self.__A[random.randint(1,self.__n)]
        self.__maxCalls = int(math.log(self.__n, 2)*2) + 2
        return self.x
    
    def lookup(self, i):
        self.__lookupCount += 1
        
        if self.__lookupCount > self.__maxCalls:
            raise ExceededLookupsError('Exceeded Maximum of {} Lookups'.format(self.__maxCalls))

            #raise Exception("Exceeded Maximum Number of Lookups")
            
        if i > self.__n:
            return None
        else:
            return self.__A[i]
    
    def lookups(self):
        return self.__lookupCount

#End findXinA functions
#################################

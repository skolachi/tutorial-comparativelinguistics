"""Python implementation of Edit distance
"""
import math
import os
import pandas as pd
import re

def edit_distance(s1, s2):
    
    #costs holds the costs of edit operations
    costs = [[0 for inner in range(len(s2)+1)] for outer in range(len(s1)+1)]
    
    # backtrace holds the edit operations
    backtrace = [[0 for inner in range(len(s2)+1)] for outer in range(len(s1)+1)]

    # Numeric coding for operations: OK- no change, SUB- substitution, INS- insertion, DEL- deletion
    OP_OK = 0
    OP_SUB = 1
    OP_INS = 2
    OP_DEL = 3
    
    # Uniform penalty, can have different penalty for different operations
    DEL_PENALTY = 1
    INS_PENALTY = 1
    SUB_PENALTY = 1
    
    # Initialize first column with index of reference
    for i in range(1, len(s1)+1):
        costs[i][0] = DEL_PENALTY*i
        backtrace[i][0] = OP_DEL
        
    # Initialize first row with index of hypothesis
    for j in range(1, len(s2) + 1):
        costs[0][j] = INS_PENALTY * j
        backtrace[0][j] = OP_INS
    
    # Levenshtein distance computation
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                costs[i][j] = costs[i-1][j-1]
                backtrace[i][j] = OP_OK
            else:
                substitutionCost = costs[i-1][j-1] + SUB_PENALTY # penalty is always 1
                insertionCost    = costs[i][j-1] + INS_PENALTY   # penalty is always 1
                deletionCost     = costs[i-1][j] + DEL_PENALTY   # penalty is always 1
                
                costs[i][j] = min(substitutionCost, insertionCost, deletionCost)
                if costs[i][j] == substitutionCost:
                    backtrace[i][j] = OP_SUB
                elif costs[i][j] == insertionCost:
                    backtrace[i][j] = OP_INS
                else:
                    backtrace[i][j] = OP_DEL
                
    # backtrace the best route
    i = len(s1)
    j = len(s2)
    numSub = 0
    numDel = 0
    numIns = 0
    numCor = 0
    edits = []
    while i > 0 or j > 0:
        if backtrace[i][j] == OP_OK:
            numCor += 1
            i-=1
            j-=1
            edits.append(["OK",s1[i],s2[j],i,'|'.join(s1),'|'.join(s2)])
        elif backtrace[i][j] == OP_SUB:
            numSub +=1
            i-=1
            j-=1
            edits.append(["SUB",s1[i],s2[j],i,'|'.join(s1),'|'.join(s2)])
        elif backtrace[i][j] == OP_INS:
            numIns += 1
            j-=1
            edits.append(["INS","****",s2[j],i,'|'.join(s1),'|'.join(s2)])
        elif backtrace[i][j] == OP_DEL:
            numDel += 1
            i-=1
            edits.append(["DEL",s1[i],"****",i,'|'.join(s1),'|'.join(s2)])

    edits = reversed(edits)
    editDistance = round( (numSub + numDel + numIns) / (float) (len(s1)), 3)
    
    return editDistance, edits


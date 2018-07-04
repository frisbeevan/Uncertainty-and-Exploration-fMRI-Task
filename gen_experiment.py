import os
import sys
import csv
from numpy.random import shuffle, seed, normal, uniform
import numpy as np
import math

nSubjects = 2
nRuns = 8
nBlocks = 4
nTrials = 10
prefix = 'uep'
conds = [[0,0], [1,1], [1,0], [0,1]]
L = ['S', 'R']
sd0 = math.sqrt(100)
sd = [0, math.sqrt(16)]
choiceDuration = 2
feedbackDuration = 1
ibi = 6 #interblock interval *BEFORE* each block starts IMPORTANT: This should match psychopy
iri = 10 #interrun interval *BEFORE* each run starts IMPORTANT: This should match psychopy



def nrand(m,sd):
    if sd == 0:
        return m;
    else:
        return round(normal(m, sd))

def gen(pilot):
    for s in range(nSubjects + 1): #subject zero is the practice subject
        if pilot:
        	subjId = '%sP%03d' % (prefix,s)
        else:
        	subjId = '%s%03d' % (prefix,s)
        subjFname = os.path.join('csv', '%s.csv' % subjId)
        with open(subjFname, 'w') as subjF:
            subjF.write('runFilename\n')

            for r in range(1, nRuns + 1): 
                runFname = os.path.join('csv', '%s_run%d.csv' % (subjId, r))
                subjF.write(runFname +'\n')
                with open(runFname, 'w') as runF:
                    runF.write('blockFilename\n')
                    c = [0,1,2,3]  # c is order of conditions
                    shuffle(c)
                    assert len(c) == nBlocks #just to make sure length of these = 4
                    assert len(conds) == nBlocks
                    if pilot:
                        isiDuration = uniform(1, 3, (nBlocks, nTrials))
                        itiDuration = uniform(2, 4, (nBlocks, nTrials))
                    else:
                        isiDuration = uniform(1, 3, (nBlocks, nTrials))
                        itiDuration = uniform(5, 7, (nBlocks, nTrials))

                    stimOnset = iri 

                    colors = [0,1,2,3,4,5,6,7] #shuffles color palette so that each option in each block has a different color
                    shuffle(colors)
                    assert len(colors) == nBlocks*2


                    for b in range(1, nBlocks + 1):
                        blockFname = os.path.join('csv', '%s_run%d_block%d.csv' % (subjId, r, b))
                        runF.write(blockFname + '\n')
                        with open(blockFname, 'w') as blockF:
                            cols = ['subjectId', 'runId', 'blockId', 'trialId', 'condition', 'leftAnswer',
                                'rightAnswer', 'choiceDuration', 'isiDuration', 'feedbackDuration',
                                'itiDuration', 'stimOnset', 'itiOffset', 'leftColor', 'rightColor']
                            blockF.write(','.join(cols) + '\n')
                            k1 = conds[c[b-1]][0]
                            k2 = conds[c[b-1]][1]
                            mu = [nrand(0,sd0), nrand(0, sd0)]

                            leftColor = colors[b*2-2]
                            rightColor = colors[b*2-1]


                            
                            print mu
                            condition = L[k1] + L[k2]
                            stimOnset = stimOnset + ibi

                            for t in range(1, nTrials+1):
                                leftAnswer = nrand(mu[0], sd[k1])
                                rightAnswer = nrand(mu[1], sd[k2])
                                itiOffset = stimOnset + choiceDuration + isiDuration[b-1, t-1] + feedbackDuration + itiDuration[b-1, t-1]

                                row = [subjId, r, b, t, condition, leftAnswer, 
                                    rightAnswer, choiceDuration, isiDuration[b-1, t-1], feedbackDuration, 
                                    itiDuration[b-1, t-1], stimOnset, itiOffset, 
                                    leftColor, rightColor]
                                blockF.write(','.join(str(x) for x in row) + '\n')
                                stimOnset = itiOffset




if __name__ == "__main__":

    seed(129523)

    gen(True)
    gen(False)

    
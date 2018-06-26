#!/usr/bin/env python
# encoding: utf-8
"""
parseGenome.py

Created by www on  8:40 pm, Oct 01, 2017
"""
import sys
import os

 
def loadFile(inputFile, minDistance, positions, outputFile):
    o   = open(outputFile, 'w+')
    directions  = {
                    'lsc1ir1ssc1ir1' : 0,
                    'lsc1ir0ssc0ir1' : 0,
                    'lsc1ir0ssc0ir0' : 0,
                    'lsc0ir0ssc0ir1' : 0,
                    'lsc0ir0ssc0ir0' : 0,
                    'lsc1ir1ssc1ir0' : 0, 
                    'lsc0ir0ssc1ir0' : 0,
                    'lsc0ir0ssc1ir1' : 0,
                    'lsc0ir1ssc1ir1' : 0,
                    'lsc0ir1ssc1ir0' : 0,
                    'lsc1ir1ssc0ir1' : 0,
                    'lsc1ir1ssc0ir0' : 0,
                    'lsc0ir1ssc0ir0' : 0,
                    'lsc0ir1ssc0ir1' : 0,
                    'lsc1ir0ssc1ir1' : 0,
                    'lsc1ir0ssc1ir0' : 0,
                  }
    atypicals = [
                    'lsc1ir1ssc1ir1',
                    'lsc1ir0ssc0ir0',
                    'lsc0ir0ssc0ir0',
                    'lsc1ir1ssc1ir0',
                    'lsc0ir0ssc1ir0',
                    'lsc0ir1ssc1ir1',
                    'lsc0ir1ssc1ir0',
                    'lsc1ir1ssc0ir1',
                    'lsc1ir1ssc0ir0',
                    'lsc0ir1ssc0ir0',
                    'lsc0ir1ssc0ir1',
                    'lsc1ir0ssc1ir0'
                 ]

    seqNames       = {}
    with open(inputFile) as f:
        for line in f:
            line    = line.strip()
            if not line:
                continue
            info    = line.split()
            seqName = info[0]
            target  = info[5]
            #target start/end on original strand
            start   = int(info[7]) 
            end     = int(info[8]) 
            
            maxPoint    = len(positions)
            i           = 0
            while i < maxPoint - 3:
                pointA  = positions[i] - minDistance
                pointB  = positions[i + 1] - minDistance

                pointC  = positions[i + 3] + minDistance
                if pointA <= start < pointB:
                    if pointC <= end:
                        #because double up the genome, the read can map twice to the genome, "names" can aviod calculating one mapping twice.
                        if not target in seqNames:
                            seqNames[target]      = {}
                        if not seqName in seqNames[target]:
                            seqNames[target][seqName] = ''
                            directions[target] += 1 
                        break
                    else:
                        i += 1
                else:
                    i += 1

    #output result

    o.write('Typical structures:\n')
    o.write('lsc0ir0ssc0ir1\t%d\n'  % directions['lsc0ir0ssc0ir1'])
    o.write('lsc1ir0ssc1ir1\t%d\n'  % directions['lsc1ir0ssc1ir1'])
    o.write('lsc1ir0ssc0ir1\t%d\n'  % directions['lsc1ir0ssc0ir1'])
    o.write('lsc0ir0ssc1ir1\t%d\n'  % directions['lsc0ir0ssc1ir1'])
    sameDirection   = directions['lsc0ir0ssc0ir1'] + directions['lsc1ir0ssc1ir1']
    diffDirection   = directions['lsc0ir0ssc1ir1'] + directions['lsc1ir0ssc0ir1']
    o.write('\n')
    o.write('Number of read support that long single copy and short single copy have same direction:\t%d\n' % sameDirection)
    o.write('Number of read support that long single copy and short single copy have different direction:\t%d\n' % diffDirection)

    o.write('\n')
    o.write('\n')
    o.write('Atypical structures:\n')
    for atypical in atypicals:
        o.write('%s\t%d\n' % (atypical, directions[atypical])) 

    o.close()


def main():
    inputFile   = sys.argv[1]
    outputFile  = sys.argv[2]
    lsc         = int(sys.argv[3])
    ssc         = int(sys.argv[4])
    ir          = int(sys.argv[5])
    minDistance = 2000


    positions   = []
    positions.append(1)
    positions.append(lsc)
    positions.append(lsc + ir)
    positions.append(lsc + ir + ssc)
    positions.append(lsc + ir + ssc + ir)
    positions.append(lsc + ir + ssc + ir + lsc)
    positions.append(lsc + ir + ssc + ir + lsc + ir)
    positions.append(lsc + ir + ssc + ir + lsc + ir + ssc)
    positions.append(lsc + ir + ssc + ir + lsc + ir + ssc + ir)

    loadFile(inputFile, minDistance, positions, outputFile)

if __name__ == '__main__':
    main()


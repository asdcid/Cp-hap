#!/usr/bin/env python
# encoding: utf-8
"""
parseGenome.py

Created by www on  8:40 pm, Oct 01, 2017
"""
import sys
import os

 
def getLength(genomeFile):
    seqs    = {'lsc' : '',
               'ssc' : '',
               'ir'  : ''
              }

    with open(genomeFile) as f:
        for line in f:
            line    = line.strip()
            if not line:
                continue
            if line[0] == '>':
                if line[1 : ]   == 'lsc':
                    seq     =  'lsc'
                elif line[1 : ] == 'ssc':
                    seq     = 'ssc'
                elif line[1 : ] == 'ir':
                    seq     = 'ir'
                continue
            seqs[seq] += line

    lsc = len(seqs['lsc'])
    ssc = len(seqs['ssc'])
    ir  = len(seqs['ir'])

    return lsc, ssc, ir

def loadFile(alignmentFile, minDistance, positions, outputFile):
    o   = open(outputFile, 'w+')
    directions  = {}

    seqNames       = {}
    with open(alignmentFile) as f:
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
                        if not target in directions:
                            directions[target] = 0
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
    o.write('Structure_name\tnumber_of_supported_reads\n')
    for direction in directions:
        o.write('%s:\t%s\n' % (direction, directions[direction]))


    o.close()


def main():
    genomeFile      = sys.argv[1]
    outputFile      = sys.argv[2]
    alignmentFile   = sys.argv[3]
    minDistance = 2000

    lsc, ssc, ir = getLength(genomeFile)


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

    loadFile(alignmentFile, minDistance, positions, outputFile)

if __name__ == '__main__':
    main()


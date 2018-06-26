#!/usr/bin/env python
# encoding: utf-8
"""

Created by www on 12:58 am, May 31, 2017
"""
import sys
import os

complement = {'A' : 'T', 'C' : 'G', 'G' : 'C', 'T' : 'A', 'N' : 'N'} 

def reverse_complement(seq):    
    bases = list(seq) 
    bases = reversed([complement.get(base,base) for base in bases])
    bases = ''.join(bases)
    return bases


 
def loadFile(inputFile, lscLength, sscLength, irLength):
    irs = {'ir0' : '',
           'ir1' : ''
          }
    sscs = {'ssc0' : '', 
            'ssc1' : ''
           }
    lscs = {'lsc0' : '',
            'lsc1' : ''
           }
    seqs = {}
    seq  = ''
    with open(inputFile) as f:
        for line in f:
            line    = line.strip()
            if not line:
                continue
            if line[0] == '>':
                continue
            seq += line
        
    lsc0 = seq[ : lscLength]
    lsc1 = reverse_complement(seq[ : lscLength])
    lscs['lsc0'] = lsc0
    lscs['lsc1'] = lsc1

    ir0 = seq[lscLength : lscLength + irLength]
    ir1 = reverse_complement(seq[lscLength : lscLength + irLength])
    irs['ir0'] = ir0
    irs['ir1'] = ir1
    
    ssc0 = seq[lscLength + irLength : lscLength + irLength + sscLength]
    ssc1 = reverse_complement(seq[lscLength + irLength : lscLength + irLength + sscLength])
    sscs['ssc0'] = ssc0
    sscs['ssc1'] = ssc1
    
    for lscDirection in lscs:
        for sscDirection in sscs:
            for irDirectionA in irs:
                for irDirectionB in irs:
                    seqs[lscDirection + irDirectionA + sscDirection + irDirectionB] = lscs[lscDirection] + irs[irDirectionA] + sscs[sscDirection] + irs[irDirectionB] + lscs[lscDirection] + irs[irDirectionA] + sscs[sscDirection] + irs[irDirectionB]

    return seqs

def output(outputDir, seqs):
    with open(outputDir, 'w+') as o:
        for name in seqs:
            o.write('>%s\n%s\n' % (name, seqs[name]))
    

def main():
    inputFile   = sys.argv[1]
    outputDir   = sys.argv[2]
    lscLength   = int(sys.argv[3])
    sscLength   = int(sys.argv[4])
    irLength    = int(sys.argv[5])
    seqs    = loadFile(inputFile, lscLength, sscLength, irLength)
    output(outputDir, seqs) 
 
if __name__ == '__main__':
    main()


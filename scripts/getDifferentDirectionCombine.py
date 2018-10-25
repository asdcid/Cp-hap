#!/usr/bin/env python
# encoding: utf-8
"""

Created by www on 12:58 am, May 31, 2017
"""
from __future__ import print_function
import sys
import os

complement_dict = { 'A' : 'T', 
                    'C' : 'G', 
                    'G' : 'C', 
                    'T' : 'A', 
                    'N' : 'N',
                    'a' : 't',            
                    'c' : 'g',            
                    'g' : 'c',            
                    't' : 'a',            
                    'n' : 'n'            
                  } 

def reverse_complement(seq):    
    bases = list(seq) 
    bases = [complement_dict.get(base,base) for base in bases]
    bases = bases[ : : -1]
    bases = ''.join(bases)
    return bases

def complement(seq):    
    bases = list(seq) 
    bases = [complement_dict.get(base,base) for base in bases]
    bases = ''.join(bases)
    return bases

def reverse(seq):
    bases = seq[ : : -1]
    return bases
 
def loadFile(genomeFile):

    lscs    = {}
    sscs    = {}
    irs     = {}

    seqs    = {'lsc' : '',
               'ssc' : '',
               'ir'  : ''
              }

    genomes                     = {}
    genomes_ori                 = {}
    genomes_noDuplicate         = {}
    names                       = {}

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
                else:
                    print('ERROR: The number of sequence in genome fasta file must be "lsc", "ssc" or "ir"')
                    sys.exit()
                continue
            seqs[seq] += line
    for seq in seqs:
        if len(seqs[seq]) == 0:
            print('ERROR: The length of %s is 0, please check the format of genome fasta file' % seq)
            sys.exit(1)
    lscs['LSC_']    = seqs['lsc']
    lscs['LSCr_']   = reverse(seqs['lsc'])
    lscs['LSCc_']   = complement(seqs['lsc'])
    lscs['LSCrc_']  = reverse_complement(seqs['lsc'])

    sscs['_SSC_']    = seqs['ssc']
    sscs['_SSCr_']   = reverse(seqs['ssc'])
    sscs['_SSCc_']   = complement(seqs['ssc'])
    sscs['_SSCrc_']  = reverse_complement(seqs['ssc'])

    irs['IR']      = seqs['ir']
    irs['IRr']     = reverse(seqs['ir'])
    irs['IRc']     = complement(seqs['ir'])
    irs['IRrc']    = reverse_complement(seqs['ir'])
    
    for lscDirection in lscs:
        for sscDirection in sscs:
            for irDirectionA in irs:
                #for irDirectionB in irs:
                
                #assume the IR is always inverted
                if irDirectionA == 'IR':
                    irDirectionB = 'IRrc' 
                elif irDirectionA == 'IRrc':
                    irDirectionB = 'IR' 
                elif irDirectionA == 'IRr':
                    irDirectionB = 'IRc' 
                elif irDirectionA == 'IRc':
                    irDirectionB = 'IRr' 
                genomes[lscDirection + irDirectionA + sscDirection + irDirectionB]  = lscs[lscDirection] + irs[irDirectionA] + sscs[sscDirection] + irs[irDirectionB] + lscs[lscDirection]
                genomes_ori[lscDirection + irDirectionA + sscDirection + irDirectionB]  = lscs[lscDirection] + irs[irDirectionA] + sscs[sscDirection] + irs[irDirectionB]

    #remove duplicate genomes
    genome_rc = {}
    for name in genomes:
        genome_rc[name] = reverse_complement(genomes[name])

    for name in genome_rc:
        seq = genome_rc[name]
        for nameB in genomes:
            if seq  == genomes[nameB]:
                key     = [name, nameB]
                key.sort()
                key     = '%s+%s' % (key[0], key[1])
                names[key] = ''
                break
    #double-up the genome, in case some reads mapped to the "cut point"
    for key in names:
        name    = key.split('+')[0]
        genomes_noDuplicate[name]   = genomes_ori[name] + genomes_ori[name]

    return genomes_noDuplicate

def output(outputFile, genomes):
    with open(outputFile, 'w+') as o:
        for name in genomes:
            o.write('>%s\n%s\n' % (name, genomes[name]))
    

def main():
    genomeFile      = sys.argv[1]
    outputFile      = sys.argv[2]

    genomes         = loadFile(genomeFile)
    output(outputFile, genomes) 
 
if __name__ == '__main__':
    main()


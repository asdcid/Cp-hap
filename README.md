# Single-copy-direction-chloroplast
Estimate the ratio of different directions of single copy in the chloroplast genome. 

# Requirement
python2.7

minimap2

# Introduction


# Usage
1. Change this section in run.sh
'''
#############################################################
#the path of long-reads, reads can be fastq(fq), fasta(fa), gzip or not, such as /path/long-read.fa
reads=
#the path of chloroplast genome, chloroplast genome should be in fasta(fa) format, not gzip, such as /path/genome.fa
chloroplastGenome=
#the path of output dir, such as /path/summary
outputDir=
#length of long single copy, must be integer, such as 88787
lengthLongSingleCopy=
#length of short single copy, must be integer, such as 18421
lengthShortSingleCopy=
#length of invert repeat, must be integer, such as 26367
lengthInvertRepeat=
#read type, 'PacBio' or 'ONT' only, such as ONT
readType=
#how many threads you want to use, such as 10
threads=
#############################################################
'''

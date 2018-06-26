# Single-copy-direction-chloroplast
Estimate the ratio of different directions of single copy in the chloroplast genome. 

# Requirement
python2.7 or higher

minimap2

# Introduction


# Usage
1. Copy run.sh, getDifferentDirectionCombine.py and parse.py to your working directory. These three scripts should be under the same directory, otherwise they don't work.

2. Set the path of minimap2 in run.sh, change the /path/of/minimap2/ to your minimap install path. If your minimap2 installed systemic, just delete the line "export PATH='/path/of/minimap2/':$PATH'.   
```
#set path of minimap2
export PATH='/path/of/minimap2/':$PATH
```
3. Change this section in run.sh
```
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
```

4. run run.sh
```
./run.sh
```
The final result will be $outputDir/result_$readName_$chloroplastGenomeName.

## Run a test
Simply change the minimap2 path in run_test.sh as describe above, then run run_test.sh. The final result is test/result_reads.fa_Epau.format.fa.
```
./run_test.sh
```

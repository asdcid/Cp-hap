#!/bin/bash

#if this script has every error, exit
set -e

#set path of minimap2
export PATH='/home/raymond/devel/miniasm/minimap2/':$PATH

#############################################################
#the path of long-reads, reads can be fastq(fq), fasta(fa), gzip or not, such as /path/long-read.fa
reads='testData/reads.fa' 
#the path of chloroplast genome, chloroplast genome should be in fasta format, not gzip, such as /path/genome.fa. The chloroplast genome file should only have three sequences, named as 'lsc', 'ssc' and 'ir' (see testData/Epau.format.fa as an example). It doesn't matter which oritentation is for lsc, ssc and ir.
chloroplastGenome='testData/Epau.format.fa' 
#the path of output dir, such as /path/summary
outputDir='test'
#read type, 'PacBio' or 'ONT' only, such as ONT
readType=ONT
#how many threads you want to use, such as 10
threads=20
#############################################################



#check argument
if [ $readType != 'PacBio' -a $readType != 'ONT' ]   
then
    echo "ERROR: readType must be PacBio or ONT."
    exit 1
elif [ $readType == 'PacBio' ]
then
    #require for minimap2
    readType='map-pb'
elif [ $readType == 'ONT' ]
then
    #require for minimap2
    readType='map-ont'
fi


mkdir -p $outputDir

#minimap2 output
minimapOutput=$outputDir/$(basename $reads).paf
#combinations of different directions of single copy
reference=$outputDir/dir_directions_$(basename $chloroplastGenome)
#final output result
outputFile=$outputDir/result_$(basename $chloroplastGenome)_$(basename $reads)

#get combinations of different direction of single copy
echo "creating different references"
python scripts/getDifferentDirectionCombine.py \
    $chloroplastGenome \
    $reference 

#run minimap2
echo "mapping long-reads to reference using minimap2"
minimap2 \
    -x $readType \
    --secondary=no \
    -t $threads \
    -L \
    -c \
    $reference \
    $reads > $minimapOutput

#check orientation ratio
echo "parsing result"
python scripts/parse.py \
    $chloroplastGenome \
    $outputFile \
    $minimapOutput \
    1000





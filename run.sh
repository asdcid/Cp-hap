#!/bin/bash

#$ -pe threads 20
#$ -cwd
#$ -N default


#if this script has every error, exit
set -e

#set path of minimap2
export PATH='/path/of/minimap2/':$PATH

#############################################################
#reads can be fastq(fq), fasta(fa), gzip or not, such as /path/long-read.fa
reads='query/blasr_RB7_C4.fasta' 
#chloroplast genome should be in fasta format, not gzip, such as /path/genome.fa
chloroplastGenome='../../assembly/ref/Epau.format.fa' 
#the path of output dir, such as /path/summary
outputDir='result'
#length of long single copy, must be integer, such as 88787
lengthLongSingleCopy=88787 
#length of short single copy, must be integer, such as 18421
lengthShortSingleCopy=18421
#length of invert repeat, must be integer, such as 26367
lengthInvertRepeat=26367 
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
minimapOutput=$outputDir/$(basename $reads).pad
#combinations of different directions of single copy
reference=$outputDir/dir_directions_$(basename $chloroplastGenome)
#final output result
outputFile=$outputDir/result_$(basename $reads)_$(basename $chloroplastGenome)

#get combinations of different direction of single copy
echo "creating different references"
./getDifferentDirectionCombine.py \
    $chloroplastGenome \
    $reference \
    $lengthLongSingleCopy \
    $lengthShortSingleCopy \
    $lengthInvertRepeat 

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
./parse.py \
    $minimapOutput \
    $outputFile \
    $lengthLongSingleCopy \
    $lengthShortSingleCopy \
    $lengthInvertRepeat 





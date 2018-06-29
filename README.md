# Chloroplast-genome-single-copy-orientation-ratio-detection
Detect the ratio of different orientations of single copys in the chloroplast genome. 

## Requirement
python2.7 or higher

minimap2 (https://github.com/lh3/minimap2)



## Installation
No installation required, just download the pipeline from github.
```
git clone https://github.com/asdcid/Chloroplast-genome-single-copy-orientation-ratio-detection.git
```

## Usage
1. Copy **run.sh**, **getDifferentDirectionCombine.py** and **parse.py** to your working directory. These three scripts should be under the same directory, otherwise they don't work.

2. Set the path of minimap2 in run.sh, change the '/path/of/minimap2/' to your minimap install path. If your minimap2 installed systemic, just delete the line "export PATH='/path/of/minimap2/':$PATH'.   
```
#set path of minimap2
export PATH='/path/of/minimap2/':$PATH
```
3. Change this section in run.sh
```
#############################################################
#the path of long-reads, reads can be fastq(fq), fasta(fa), gzip or not, such as /path/long-read.fa
reads=
#the path of chloroplast genome, chloroplast genome should be in fasta format, not gzip, such as /path/genome.fa. The chloroplast genome file should only have three sequences, named as 'lsc', 'ssc' and 'ir' (see testData/Epau.format.fa as an example). It doesn't matter which oritentation is for lsc, ssc and ir.
chloroplastGenome=
#the path of output dir, such as /path/summary
outputDir=
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
Simply point out the minimap2 path in run_test.sh as describe above, then run run_test.sh. The final result is test/result_reads.fa_Epau.format.fa.
```
./run_test.sh
```

## Background
The chloroplast genome is a double-stranded DNA circular molecule of around 120 kb – 160 kb in size in most plants，The structure of chloroplast genome is highly conserved among plants, and usually consists of a long single copy and a short single copy region, separated by two identical inverted repeat regions.The length of inverted repeats usually ranges from 10 to 30 kb, although in extreme cases can be as short as 114 bp or as long as 76 kb. However, the orientation of the two single copy (long/short) can be the same or different. In general, the ratio between the two orientations should be 50% vs 50%. 
<p>
  <img src="https://github.com/asdcid/figures/blob/master/Chloroplast-genome-single-copy-orientation-ratio-detection/circular_different_orientation.jp" />
 </p>

16 situtation

8 (2 is typical, other not)

pass 3 points

50 vs 50 (if got enough long-reads)

The general idea of this pipeline is that mapped all the long-reads to the 16 different combination chloroplast genomes, and then detech the number of long-read that pass three conjunctions support. Simple linearization of the reference set would risk failing to capture reads that span the point at which the genomes were circularized. To avoid this, we duplicated and concatenated the sequence of each genome in the reference set.

dis:
long-read should cover three conjunctions. 

assume cp have two invert repeats. 


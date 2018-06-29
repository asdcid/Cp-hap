# Chloroplast-genome-single-copy-orientation-ratio-detection
Detect the ratio of different orientations of single copys in the chloroplast genome. 


## Background
The chloroplast genome is a double-stranded DNA circular molecule of around 120 kb – 160 kb in size in most plants，The structure of chloroplast genome is highly conserved among plants, and usually consists of a long single copy and a short single copy region, separated by two identical inverted repeat regions.The length of inverted repeats usually ranges from 10 to 30 kb, although in extreme cases can be as short as 114 bp or as long as 76 kb. However, the orientation of the two single copys (long/short) can be the same or different. In general, the ratio between the two orientations should be 50% vs 50%. 
<p>
  <img src="https://github.com/asdcid/figures/blob/master/Chloroplast-genome-single-copy-orientation-ratio-detection/orientation.jpg" />
 </p>

Long single copy, short single copy or inverted repeat can have four different orientations: original, reverse(r), complement(c) and reverse complement(rc). Technically, there are 256 different orientation combinations. However, half of them (128) is the complementary strand of the other half. Therefore, only 128 possible structures.
<p>
  <img src="https://github.com/asdcid/figures/blob/master/Chloroplast-genome-single-copy-orientation-ratio-detection/equal_structure.png" />
 </p>

So far, only two structures are observed: the single copys (long/short) have same orientation, have different orientations.  

In order to detech whether only two different structures present in the chloroplast genome, and compare the ratio between them, this pipeline first creates a reference set containing all 128 different structures, and then map all long-reads to the genome file, filtered out reads failed to cover at least three conjunctions (lsc/ir, ir/ssc, ssc/ir or ir/lsc), calcuated the number of supported read for each structure.

The reads must be long enough to cover at least three conjunctions, otherwise it cannot unique map to one structure (The long single copy is duplicated here to make it clear).
<p>
  <img src="https://github.com/asdcid/figures/blob/master/Chloroplast-genome-single-copy-orientation-ratio-detection/three_conjunction.jpg" />
 </p>

In addition, simple linearization of the chloroplast genome would risk failing to capture reads that span the point at which the genomes were circularized. To avoid this, we duplicated and concatenated the sequence of each genome in the reference set.


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

Example format of chloroplast genome:
```
>lsc
XXXX
>ssc
XXXX
>ir
XXXX
```

The chloroplast genome file should be a fasta file containing three sequences: lsc (long single copy), ssc (short single copy) and ir (inverted repeat). The sequence names must be "lsc", "ssc" and "ir". The sequences can be in one line or multiple lines. It is no requirment for the direction of each sequence.

We assume the two inverted repeats are identical. If there are only few base pairs difference between the two inverted repeats, just choose one of them. If the difference is huge, you need to create the different orientation structure combination genome file by yourself, and then run minimap2 and parse.py. For the chloroplast genome which only has one inverted repeats, this pipeline may not work well.


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

### OutputFiles explanation
Using the test result as an example, there are three outputFiles: 

50 vs 50 (if got enough long-reads)

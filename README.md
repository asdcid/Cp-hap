# Chloroplast-genome-haplotype-ratio-detection (Cp-hap)
Detect the ratio of different orientations of single copies in the chloroplast genome. 

## Background
The chloroplast genome is a double-stranded DNA circular molecule of around 120 kb – 160 kb in size in most plants. The structure of chloroplast genome is highly conserved among plants, and usually consists of a long single copy and a short single copy region, separated by two identical inverted repeat regions. The length of inverted repeats usually ranges from 10 to 30 kb, although in extreme cases can be as short as 114 bp or as long as 76 kb, and in some species only one inverted repeat presents. However, the orientations of the two single copies (long/short) can be identical or different for those chloroplast genomes which have two inverted repeats.  
<p>
  <img src="https://github.com/asdcid/figures/blob/master/Chloroplast-genome-single-copy-orientation-ratio-detection/orientations.jpg" />
 </p>

Long single copy, short single copy or inverted repeat can have four different orientations: original, reversed(r), complementary(c) and reversed complementary(rc). Technically, there are 256 different orientation combinations. However, half of them (128) are the complementary strand of the other half. Therefore, there are only 128 possible structures.
<p>
  <img src="https://github.com/asdcid/figures/blob/master/Chloroplast-genome-single-copy-orientation-ratio-detection/equal_structure.png" />
 </p>

So far, we call the two common structures (the two single copies (long/short) with the identical orientation and with different orientations, the repeat regions are inverted) as haplotype A and haplotype B here. 

<p>
  <img src="https://github.com/asdcid/figures/blob/master/Chloroplast-genome-single-copy-orientation-ratio-detection/equal_structure.png" />
 </p>


In order to detect whether only two different structures present in the chloroplast genome, and compare the ratio between them, this pipeline first created a reference set containing all 128 different chloroplast genome structures. Then we mapped all long-reads to the genome file, filtered out reads failed to cover at least three conjunctions (lsc/ir, ir/ssc, ssc/ir or ir/lsc), and calcuated the number of supported reads for each structure.

To uniquely identify one of these 128 structures, a single sequencing read would need to cover at least some parts of all four regions (LSC, SSC and the two IR regions), for which the read would need to be at least 30-50 kb. This is because to cover all four regions, at a minimum a read must entirely cover the SSC (~20 kb) region and one IR region (10-30 kb) and at least partially cover the LSC region and the other IR region. However, there are not many reads have this length (~50kb). Therefore, Cp-hap pipeline assumes by default that the two large repeat regions are always inverted. When assuming that the IR regions are always inverted, there are only 32 uniquely identifiable chloroplast genome structural haplotypes. 

<p>
  <img scr="https://github.com/asdcid/figures/blob/master/Chloroplast-genome-single-copy-orientation-ratio-detection/Fig S1. 32 chloroplast genome sturctures.png" />
</p>

In this situation, a read only needs to entirely cover one IR region and partially cover the two adjacent LSC and SSC regions to provide evidence to uniquely identify one of the 32 structures.

<p>
  <img scr="https://github.com/asdcid/figures/blob/master/Chloroplast-genome-single-copy-orientation-ratio-detection/mapped.png"/>
</p>


In addition, the simple linearization of the chloroplast genome would risk failing to capture reads that span the point at which the genomes were circularized. To avoid this, we duplicated and concatenated the sequence of each genome in the reference set.


However, we acknowledge that the IR regions are not always the case. For example, the large repeat regions are positioned in-line instead of inverted in Selaginella tamariscina chloroplast genome (18). In cases such as this, Cp-hap pipeline is also able to figure out the structure. Here, we provide an example that how Cp-hap pipeline confirms a chloroplast genome with atypical structure, such as a paired of in-line repeats (Fig. S3C). Since Cp-hap duplicates and concatenates all default 32 structures (with IRs), reads from chloroplast genome with in-line repeats are able to map to Block A and/or C region of LSC_IR_SSC_IRrc structure (one of the 32 default structure in Cp-hap pipeline), or Block B region of LSC_IRrc_SSC_IR structure (the other default structure in Cp-hap pipeline). Those reads are impossible to map to Block B region of LSC_IR_SSC_IRrc, or Block A or C region of LSC_IRrc_SSC_IR. Therefore, if some reads only map to Block A and/or C region of LSC_IR_SSC_IRrc and Block B region of LSC_IRrc_SSC_IR, it suggests that the chloroplast genome acquires in-line repeats. 


## Requirement
python2.7 or higher

minimap2 (https://github.com/lh3/minimap2)


## Installation
No installation required, just download the pipeline from github.
```
git clone https://github.com/asdcid/Cp-hap.git
```

## Usage
1. Set the path of minimap2 , if your minimap2 not installed systemic 
```
export PATH='/path/of/minimap2/':$PATH
```
2. run Cp-hap.sh
```
Usage: bash Cp-hap.sh -r reads -g chloroplastGenome.fa -o outputDir [options]
Required:
    -r      the path of long-read file in fa/fq format, can be compressed(.gz).
    -g      the path of chloroplast genome, chloroplast genome should be in fa format, not gzip. The chloroplast genome file should only have three sequences, named as 'lsc', 'ssc' and 'ir' (see testData/Epau.format.fa as an example). It does not matter which oritentation is for lsc, ssc and ir.
    -o      the path of outputDir.
Options:
    -t      number of threads. Default is 1.
    -x      readType, only can be map-pb (PacBio reads) or map-ont (Nanopore reads). Default is map-pb.
    -d      minimun distance of exceeding the first and last conjunctions (such as lsc/ir and ir/ssc). 1 means 1 bp, 1000 means 1 kb. Default is 1000.
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

The chloroplast genome file should be a fasta file containing three sequences: lsc (long single copy), ssc (short single copy) and ir (inverted repeat). The sequence names must be "lsc", "ssc" and "ir". The sequences can be in one line or multiple lines. It is no requirement for the direction of each sequence.

We assume the two inverted repeats are identical. If there are only few base pairs difference between the two inverted repeats, just choose one of them. If the difference is huge, you need to create the reference set by yourself, and then run minimap2 and parse.py. For the chloroplast genome which only has one inverted repeat, this pipeline may not work well.


The final result will be $outputDir/result_$readName_$chloroplastGenomeName.

## Run a test
Simply point out the minimap2 path in run_test.sh as describe above, then run run_test.sh. The final result is test/result_reads.fa_Epau.format.fa.
```
./run_test.sh
```

### OutputFiles explanation
Using the test result as an example, there are three outputFiles: dir_directions_Epau.format.fa (reference set, containing 128 different chloroplast genome structures), reads.fa.pad (minimap2 outputFile) and result_Epau.format.fa_reads.fa (final result file).

In the final result file, the chloroplast genome structure is named in something like "LSC_IR_SSC_IRrc".
```
Structure name explanation
LSC:    long single copy
SSC:    short single copy
IR: invert repeat

r:  reversed sequence
c:  complementary sequence
rc: reversed complementary sequence
```

In general, only two structures will be observed, such as "LSC_IR_SSC_IRrc" (haplotype A) and "LSC_IR_SSCrc_IRrc" (haplotype B), which are the single copies (long/short) with the identical or different orientations. The orientation of inverted repeats should be identical between these two structures. And the number of reads supporting each structure should be similar (50% vs 50%) if you have enough reads covering at least three conjunctions (see above).

However, if you get two structures which are not different in the orientation of LSC/SSC (such as LSC_IR_SSC_IRrc and LSC_IRrc_SSC_IRrc), it suggests that your chloroplast genome have haplotypes which as different from the normal haplotype A and B. Under this case, the structure shown in the outputFile is not the real chloroplast haplotype. You need to manually check the mapped position of read to infer the real chloroplast genome structure (see above). For example, the Selaginella tamariscina chloroplast genome has a positioned repeats (two "inverted repeats" in the same orientation instead of inverted, LSC_IR_SSC_IR). In this case, two structure will be observed:LSCrc_IR_SSCrc_IRrc and LSC_IR_SSC_IRrc.


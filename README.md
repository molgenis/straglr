## Straglr (*S*hort-*t*andem *r*epe*a*t *g*enotyping using *l*ong *r*eads

Straglr is a tool that can be used for genome-wide scans for tandem repeat(TR) expansions or targeted genotyping using long-read alignments.

Input alignments(coordinate-sorted) against the reference genome for Straglr is expected to be generated by [Minimap2](https://github.com/lh3/minimap2).

Straglr is implemented in Python 2.7 and has been tested in Linux environment.

Straglr relies on [Tandem Repeat Finder(TRF)](https://tandem.bu.edu/trf/trf.html) for identifying TR sequences. (TRF executable must be in PATH)

Straglr can be installed via pip: 

```
pip install git+https://github.com/bcgsc/straglr.git#egg=straglr
```

Example usage:

```
python straglr.py <mm2.bam> <reference_fasta> <output.tsv> [--loci loci.bed] [--exclude skip_regions.bed] [--chroms chr] [--min_ins_size N] [--nprocs N]
```

Some common parameters:

--loci: a BED file containing loci for which only genotyping is performed. A 4 column BED format: chromosome start end repeat

--exclude: a BED file containing regions such as segmental duplications or pericentromeric regions where alignment is less reliable and analysis is preferrably skipped. This can be compiled using UCSC's "Table Browser" tool 

--chroms: space-separated list of chromosomes for which results are only obtained

--min\_ins_size: when used for searching repeat expansions, minimum insertion size for detection (<50 is not desirable as long reads are prone to small indels)

--nprocs: number of processes to use in Python's multiprocessing

Contact: [Readman Chiu](mailto:rchiu@bcgsc.ca)

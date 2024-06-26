import numpy as np
from collections import Counter
from .cluster import Cluster

class Variant:
    """
    0: chrom
    1: start
    2: end
    3: alleles
    4: repeat
    5: genotypes
    6: genotype_summary
    """
    tsv_headers = ['chrom',
                   'start',
                   'end',
                   'repeat_unit',
                   'genotype',
                   ]

    bed_headers = ['chrom', 'start', 'end', 'repeat_unit']


    @classmethod
    def set_genotype_config(cls, method=None, min_reads=None, max_num_clusters=3, eps=None, sex="female"):
        genotype_config = {'min_reads': 4, 'max_num_clusters': max_num_clusters, 'sex': sex}

        # minimum number of reads per cluster
        if min_reads is not None:
            genotype_config['min_reads'] = min_reads

        max_genotype_dict = {
         'male': {'chrX': 1},
         'female': {}
        }
        cls.clustering = Cluster(genotype_config['min_reads'], max_genotype_dict[genotype_config['sex']])

    @classmethod
    def genotype(cls, variant, report_in_size=False):
        # cluster - always use sizes
        sizes = sorted([a[4] for a in variant[3]])
        repeat_unit_len = len(variant[4])
        clusters = cls.clustering.cluster(sizes, repeat_unit_len * 2, variant[0])

        # genotype labels: mean of either copy numbers(default) or size
        for cluster in clusters:
            if report_in_size:
                alleles = cluster
            else:
                alleles = [allele[3] for allele in variant[3] if allele[4] in cluster]
            variant[5].append((np.percentile(alleles, 10), round(np.median(alleles), 1), np.percentile(alleles, 90)))

        # assign genotype to each allele
        for allele in variant[3]:
            assigned = False
            for i in range(len(clusters)):
                if allele[4] in clusters[i]:
                    allele.append(variant[5][i][1])
                    assigned = True
                    break

            # '-' assigned if read is an outlier in clustering
            if not assigned:
                allele.append('-')

    @classmethod
    def get_genotype(cls, variant):

        allele_counts = Counter([allele[-1] for allele in variant[3]])
        gt = []
        for allele in sorted([a for a in allele_counts.keys() if type(a) is not str], reverse=True) +\
                             [a for a in allele_counts.keys() if type(a) is str]:
            if allele == '-' and len(allele_counts.keys()) > 1:
                continue
            gt.append((allele, allele_counts[allele]))

        return gt

    @classmethod
    def summarize_genotype(cls, variant):
        gt = cls.get_genotype(variant)
        out = []
        for allele, support in gt:
            out.append('{}({})'.format(allele, support))
        variant[6] = ';'.join(out)

    @classmethod
    def to_tsv(cls, variant):
        sorted_genotypes = sorted(variant[5], reverse=True)
        cols = [variant[0],
                variant[1],
                variant[2],
                variant[4],
                variant[6],
                ]
        return list(map(str, cols))

    @classmethod
    def above_min_expansion(cls, variant, min_expansion, min_reads):
        ref_size = int(variant[2]) - int(variant[1]) + 1

        if variant[5]:
            n = 0
            for allele in sorted(variant[5], reverse=True):
                reads = [a for a in variant[3] if a[8] == allele and a[4] - ref_size >= min_expansion]
                n += len(reads)

            if n >= min_reads:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def update_coords(cls, variant):
        genome_starts = [a[5] for a in variant[3]]
        genome_ends = [a[6] for a in variant[3]]
        if genome_starts and genome_ends:
            variant[1] = int(np.median(genome_starts))
            variant[2] = int(np.median(genome_ends))

    @classmethod
    def summarize_alleles(cls, alleles):
        reads = []
        sizes = []
        cns = []
        starts = []
        for allele in alleles:
            reads.append(allele[0])
            sizes.append(str(allele[4]))
            cns.append(str(allele[3]))
            starts.append(str(allele[1]))

        return ','.join(reads), ','.join(cns), ','.join(sizes), ','.join(starts)

class Allele:
    """
    0: read
    1: rstart
    2: repeat
    3: copy_number
    4: size
    5: genome_start
    6: genome_end
    7: strand
    8: genotype
    """
    tsv_headers = ['read',
                   'copy_number',
                   'size',
                   'read_start',
                   'strand',
                   'allele',
                   ]

    summary_headers = ['reads',
                       'copy_numbers',
                       'sizes',
                       'read_starts',
                       ]

    @classmethod
    def to_tsv(cls, cols):
        # __init__ input order to output order
        cols_ordered = [cols[0],
                        cols[3],
                        cols[4],
                        cols[1],
                        cols[7],
                        cols[8],
                        ]
        return list(map(str, cols_ordered))

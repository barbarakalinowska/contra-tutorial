import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from scripts import sam as sam_handler


def make_plots(sam_dir):
    column_names = ["read_id", "flags_sum", "ref", "pos", "quality", "cigar",
                    "ref_aln", "aln_pos", "insert", "read_seq", "aln",
                    "opt1", "opt2", "opt3", "opt4", "opt5", "opt6", "opt7"]

    sam_paths = sam_handler.get_sam_paths(sam_dir)
    genes_count = []
    for sam_path in sam_paths:
        genes_count.append(group_genes_from_sam(sam_path, column_names))

    gene_counts_all = merge_genes_dataframes(genes_count)

    make_genes_abundance_seaborn(gene_counts_all)
    make_genes_abundance_plt(gene_counts_all)


def group_genes_from_sam(sam_path, column_names):
    aln = pd.read_csv(sam_path, delimiter="\t", names=column_names, comment="@",
                      index_col=False, compression='infer')
    aln = aln[aln['cigar'] != "*"]
    aln['gene'] = aln['ref'].str.split("_", 1, expand=True)[0]
    aln = aln.groupby('gene').size()
    aln.name = 'sample'

    return aln


def merge_genes_dataframes(genes_count):
    gene_count_0_1 = pd.merge(genes_count[0], genes_count[1], on="gene", how="outer", suffixes=['_0', '_1'])
    gene_count_2_3 = pd.merge(genes_count[2], genes_count[3], on="gene", how="outer", suffixes=['_2', '_3'])

    return pd.merge(gene_count_0_1, gene_count_2_3, on="gene")


def make_genes_abundance_seaborn(gene_count):
    path = 'output/abundance_sns.png'

    sns.set(style="whitegrid")
    data = pd.melt(gene_count)
    ax = sns.boxplot(x="variable", y="value", data=data)
    ax.set(xlabel='sample', ylabel='counts', title="Genes abundance")

    print('Saving: {}'.format(path))
    plt.savefig(path)
    plt.close()
    # plt.show()


def make_genes_abundance_plt(gene_count):
    path = 'output/abundance_plt.png'

    for sample in gene_count.columns:
        ax = sns.distplot(gene_count[sample].dropna(), kde=False, hist=True, label=sample)
    ax.set(xlabel='counts', title="Genes abundance")
    ax.legend()

    print('Saving: {}'.format(path))
    plt.savefig(path)
    plt.close()
    # plt.show()

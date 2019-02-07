import click
from Bio import SeqIO


def is_fasta_file(ctx, param, value):
    """
    :param ctx: click context
    :param param: click param
    :param value: filename
    :return: returns the filename if the extension is correct or raises BadParameter exception
    """
    if value.endswith('.fasta'):
        return value


def count_genes(fasta_file):
    genes_count = dict()
    return genes_count

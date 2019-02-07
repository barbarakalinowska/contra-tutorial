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
    else:
        raise click.BadParameter('Given file is not FASTA file')


def count_genes(fasta_file):
    genes_count = dict()
    with open(fasta_file, 'r') as fasta:
        for record in SeqIO.parse(fasta, format='fasta'):
            genes_count[record.id.split("_")[0]] = 0

    return genes_count

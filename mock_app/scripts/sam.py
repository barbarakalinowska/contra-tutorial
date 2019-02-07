import os

import click



def update_genes_count_with_many_sam_files(genes_count, sam_paths):
    genes_count_samples = dict()
    return genes_count_samples


def update_genes_count(genes_count, sam_path):
    return genes_count


def is_read_valid(read):
    return not read.is_unmapped


def get_sam_paths(sam_dir):
    """
    :param sam_dir: directory in which sam files will be searched
    :return: list of paths to sam files
    """
    return [os.path.join(sam_dir, file) for file in os.listdir(sam_dir) if file.endswith('.sam')]


def contains_sam_file(ctx, param, value):
    """
    :param ctx: click context
    :param param: click param
    :param value: click param value
    :return: value if it is a directory with at least 1 SAM file
    """
    if os.path.isdir(value) and any(file.endswith('.sam') for file in os.listdir(value)):
        return value

import click

import scripts.fasta as fasta_handler
from scripts import plot as plot_handler
from scripts import report_generator
from scripts import sam as sam_handler


@click.group()
def cli():
    pass


@cli.command()
@click.option('--sam', '-s',
              type=click.Path(exists=True, readable=True),
              callback=sam_handler.contains_sam_file,
              required=True,
              help='Directory with SAM files')
@click.option('--fasta', '-f',
              type=click.Path(exists=True, readable=True),
              callback=fasta_handler.is_fasta_file,
              required=True,
              help='Path to FASTA file')
@click.option('--plot', '-p',
              is_flag=True,
              default=False,
              required=False,
              help='If present plots will be made')
def build(sam, fasta, plot):
    genes_count = fasta_handler.count_genes(fasta)
    genes_count_samples = sam_handler.update_genes_count_with_many_sam_files(genes_count, sam_handler.get_sam_paths(sam))
    report_generator.generate_mutliple_reports(genes_count_samples)

    if plot:
        plot_handler.make_plots(sam)


if __name__ == '__main__':
    cli()

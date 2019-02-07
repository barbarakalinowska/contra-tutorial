import tempfile
import unittest

import click

from scripts import fasta


class FastaTests(unittest.TestCase):
    def test_is_fasta_file_returns_fasta_path_for_valid_file(self):
        self.assertEqual(fasta.is_fasta_file(None, None, 'file.fasta'), 'file.fasta')

    def test_is_fasta_file_raises_exception_for_invalid_file(self):
        self.assertRaises(click.BadParameter, fasta.is_fasta_file, ctx=None, param=None, value='nonfastafile.file')

    def test_count_genes(self):
        fasta_mock = tempfile.NamedTemporaryFile(mode='w', suffix='.fasta')
        fasta_mock.write(
            '> ENSG00000139083_GCAGCCAATTTACTGGAGCA\n'
            'gcagccaatttactggagca\n'
            '> ENSG00000119718_GAGCTCCGAGGAAATGGCTC\n'
            'gagctccgaggaaatggctc\n'
        )
        fasta_mock.seek(0)

        count_genes = fasta.count_genes(fasta_mock.name)
        fasta_mock.close()

        assert 'ENSG00000139083' in count_genes
        assert 'ENSG00000119718' in count_genes


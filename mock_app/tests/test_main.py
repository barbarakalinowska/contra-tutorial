import tempfile
import unittest

from click.testing import CliRunner

import main


class MainTests(unittest.TestCase):
    def test_cli_without_sam(self):
        temp_fasta = tempfile.NamedTemporaryFile(mode='r', suffix='.fasta')

        runner = CliRunner()
        result = runner.invoke(main.cli, ['build', '--fasta', temp_fasta.name])
        temp_fasta.close()

        self.assertTrue('Missing option "--sam"' in result.output)

    def test_cli_without_fasta(self):
        temp_dir = tempfile.TemporaryDirectory()
        temp_sam = tempfile.NamedTemporaryFile(suffix='.sam', dir=temp_dir.name)

        runner = CliRunner()
        result = runner.invoke(main.cli, ['build', '--sam', temp_dir.name])

        temp_sam.close()
        temp_dir.cleanup()

        self.assertTrue('Missing option "--fasta"' in result.output)


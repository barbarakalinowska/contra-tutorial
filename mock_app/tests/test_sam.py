import os
import tempfile
import unittest

import click
import pysam

from scripts import sam


class SamTests(unittest.TestCase):
    def test_update_genes_count_with_many_sam_files(self):
        sam_mock_1 = tempfile.NamedTemporaryFile(mode='w', suffix='.sam')
        sam_mock_1.write(
            '@HD	VN:1.0	SO:unsorted\n'
            '@SQ	SN:ENSG00000160469_GCCAAGGGCACCATGTCGTC	LN:20\n'
            '@PG	ID:Bowtie	VN:1.2.2	CL:"/usr/bin/bowtie-align-s --wrapper basic-0 screen_library --threads 8 -a --sam --best --strata -l 20 sample1.fq"\n'
            'M01100:32:000000000-AAD7V:1:1101:18006:1843	0	ENSG00000160469_GCCAAGGGCACCATGTCGTC	1	255	20M	*	0	0	GCCAAGGGCACCATGTCGTC	C00/////A/AA0B1FGHGE	XA:i:0	MD:Z:20	NM:i:1	XM:i:2\n'
        )
        sam_mock_1.seek(0)

        sam_mock_2 = tempfile.NamedTemporaryFile(mode='w', suffix='.sam')
        sam_mock_2.write(
            '@HD	VN:1.0	SO:unsorted\n'
            '@SQ	SN:ENSG00000171174_GATGACGTCCATGGTGTGTA	LN:20\n'
            '@PG	ID:Bowtie	VN:1.2.2	CL:"/usr/bin/bowtie-align-s --wrapper basic-0 screen_library --threads 8 -a --sam --best --strata -l 20 sample1.fq"\n'
            'M01100:32:000000000-AAD7V:1:1101:18006:1843	0	ENSG00000171174_GATGACGTCCATGGTGTGTA	1	255	20M	*	0	0	GATGACGTCCATGGTGTGTA	C00/////A/AA0B1FGHGE	XA:i:0	MD:Z:20	NM:i:1	XM:i:2\n'
        )
        sam_mock_2.seek(0)

        genes_count = {
            'ENSG00000160469': 0,
            'ENSG00000171174': 0
        }

        genes_count = sam.update_genes_count_with_many_sam_files(genes_count, [sam_mock_1.name, sam_mock_2.name])

        sam_mock_1.close()
        sam_mock_2.close()

        self.assertEqual(genes_count[os.path.basename(sam_mock_1.name).split(".")[0]]['ENSG00000160469'], 1)
        self.assertEqual(genes_count[os.path.basename(sam_mock_1.name).split(".")[0]]['ENSG00000171174'], 1)

    def test_count_genes_with_mapped_read_with_NM_1(self):
        sam_mock = tempfile.NamedTemporaryFile(mode='w', suffix='.sam')
        sam_mock.write(
            '@HD	VN:1.0	SO:unsorted\n'
            '@SQ	SN:ENSG00000160469_GCCAAGGGCACCATGTCGTC	LN:20\n'
            '@PG	ID:Bowtie	VN:1.2.2	CL:"/usr/bin/bowtie-align-s --wrapper basic-0 screen_library --threads 8 -a --sam --best --strata -l 20 sample1.fq"\n'
            'M01100:32:000000000-AAD7V:1:1101:18006:1843	0	ENSG00000160469_GCCAAGGGCACCATGTCGTC	1	255	20M	*	0	0	GCCAAGGGCACCATGTCGTC	C00/////A/AA0B1FGHGE	XA:i:0	MD:Z:20	NM:i:1	XM:i:2\n'
        )
        sam_mock.seek(0)

        genes_count = {
            'ENSG00000160469': 0
        }

        genes_count = sam.update_genes_count(genes_count, sam_mock.name)
        sam_mock.close()

        self.assertEqual(genes_count['ENSG00000160469'], 1)

    def test_count_genes_with_mapped_read_with_NM_0(self):
        sam_mock = tempfile.NamedTemporaryFile(mode='w', suffix='.sam')
        sam_mock.write(
            '@HD	VN:1.0	SO:unsorted\n'
            '@SQ	SN:ENSG00000160469_GCCAAGGGCACCATGTCGTC	LN:20\n'
            '@PG	ID:Bowtie	VN:1.2.2	CL:"/usr/bin/bowtie-align-s --wrapper basic-0 screen_library --threads 8 -a --sam --best --strata -l 20 sample1.fq"\n'
            'M01100:32:000000000-AAD7V:1:1101:18006:1843	0	ENSG00000160469_GCCAAGGGCACCATGTCGTC	1	255	20M	*	0	0	GCCAAGGGCACCATGTCGTC	C00/////A/AA0B1FGHGE	XA:i:0	MD:Z:20	NM:i:0	XM:i:2\n'
        )
        sam_mock.seek(0)

        genes_count = {
            'ENSG00000160469': 0
        }

        genes_count = sam.update_genes_count(genes_count, sam_mock.name)
        sam_mock.close()

        self.assertEqual(genes_count['ENSG00000160469'], 0)

    def test_is_read_valid_returns_true_for_valid_read(self):
        read_mock = pysam.AlignedSegment()
        read_mock.set_tag('NM', 1)

        self.assertTrue(sam.is_read_valid(read_mock))

    def test_is_read_valid_returns_false_for_invalid_read(self):
        read_mock = pysam.AlignedSegment()

        read_mock.set_tag('NM', 0)
        self.assertFalse(sam.is_read_valid(read_mock))

    def test_get_sam_paths_returns_only_list_of_sam_files(self):
        tempdir = tempfile.TemporaryDirectory(suffix='sam_dir')
        test_sam = tempfile.NamedTemporaryFile(mode='r', suffix='.sam', dir=tempdir.name)
        test_not_sam = tempfile.NamedTemporaryFile(mode='r', suffix='.file', dir=tempdir.name)

        sam_paths = sam.get_sam_paths(tempdir.name)

        self.assertTrue(test_sam.name in sam_paths)
        self.assertFalse(test_not_sam.name in sam_paths)

        test_sam.close()
        test_not_sam.close()
        tempdir.cleanup()

    def test_contains_sam_file_returns_dir_path(self):
        temp_dir = tempfile.TemporaryDirectory()
        temp_sam = tempfile.NamedTemporaryFile(suffix='.sam', dir=temp_dir.name)

        self.assertEqual(sam.contains_sam_file(None, None, temp_dir.name), temp_dir.name)

        temp_sam.close()
        temp_dir.cleanup()

    def test_if_contaitns_sam_file_raises_exception_with_empty_dir(self):
        temp_dir = tempfile.TemporaryDirectory()

        self.assertRaises(click.BadParameter, sam.contains_sam_file, ctx=None, param=None, value=temp_dir.name)

        temp_dir.cleanup()


#!/usr/bin/env python

import os
import io
import shutil
import tempfile
import unittest
import csv
import json
import mock
import filecmp
import subprocess
from datetime import datetime
import sys

from taca.analysis.analysis import *
from taca.illumina.Runs import Run, _create_folder_structure, _generate_lane_html
from taca.illumina.HiSeq_Runs import HiSeq_Run, _data_filed_conversion
from taca.illumina.HiSeqX_Runs import HiSeqX_Run, _generate_clean_samplesheet, _classify_samples, parse_10X_indexes, parse_smartseq_indexes, _generate_samplesheet_subset
from taca.illumina.MiSeq_Runs import MiSeq_Run
from taca.illumina.NovaSeq_Runs import NovaSeq_Run
from taca.illumina.NextSeq_Runs import NextSeq_Run
from flowcell_parser.classes import LaneBarcodeParser, SampleSheetParser
from taca.utils import config as conf

if sys.version_info[0] >= 3:
    unicode = str

# This is only run if TACA is called from the CLI, as this is a test, we need to
# call it explicitely
CONFIG = conf.load_yaml_config('data/taca_test_cfg.yaml')


class TestRuns(unittest.TestCase):
    """Tests for the Run base class."""
    @classmethod
    def setUpClass(self):
        """ Creates the following directory tree for testing purposes:

        tmp/
        |__ 141124_ST-COMPLETED_01_AFCIDXX
        |   |__ RunInfo.xml
        |   |__ Demultiplexing
        |   |   |__ Undetermined_S0_L001_R1_001.fastq.gz
        |   |   |__ Stats
        |   |       |__ DemultiplexingStats.xml
        |   |__ RTAComplete.txt
        |   |__ SampleSheet.csv
        |__ 141124_ST-INPROGRESS_02_AFCIDXX
        |   |__ RunInfo.xml
        |   |__ Demultiplexing
        |   |__ Demultiplexing_0
        |   |__ Demultiplexing_1
        |   |__ Demultiplexing_2
        |   |__ Demultiplexing_3
        |   |__ SampleSheet_0.csv
        |   |__ SampleSheet_1.csv
        |   |__ SampleSheet_2.csv
        |   |__ SampleSheet_3.csv
        |   |__ RTAComplete.txt
        |__ 141124_ST-INPROGRESSDONE_02_AFCIDXX
        |   |__ RunInfo.xml
        |   |__ Demultiplexing
        |   |__ Demultiplexing_0
        |   |   |__Stats
        |   |      |__ DemultiplexingStats.xml
        |   |      |__ DemuxSummaryF1L1.txt
        |   |__ Demultiplexing_1
        |   |   |__Stats
        |   |      |__ DemultiplexingStats.xml
        |   |__ Demultiplexing_2
        |   |   |__Stats
        |   |      |__ DemultiplexingStats.xml
        |   |__ Demultiplexing_3
        |   |   |__Stats
        |   |      |__ DemultiplexingStats.xml
        |   |__ SampleSheet_0.csv
        |   |__ SampleSheet_1.csv
        |   |__ SampleSheet_2.csv
        |   |__ SampleSheet_3.csv
        |   |__ RTAComplete.txt
        |__ 141124_ST-RUNNING_03_AFCIDXX
        |   |__ RunInfo.xml
        |__ 141124_ST-TOSTART_04_FCIDXXX
        |   |__ RunInfo.xml
        |   |__ RTAComplete.txt
        |__ 141124_ST-DUMMY1_01_AFCIDXX
        |   |__ RunInfo.xml
        |   |__ SampleSheet.csv
        |__ 141124_ST-COMPLEX1_01_AFCIDXX
        |   |__lots of files
        |__ archive
        """
        self.tmp_dir = os.path.join(tempfile.mkdtemp(), 'tmp')
        self.transfer_file = os.path.join(self.tmp_dir, 'transfer.tsv')

        running = os.path.join(self.tmp_dir, '141124_ST-RUNNING1_03_AFCIDXX')
        to_start = os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_FCIDXXX')
        in_progress = os.path.join(self.tmp_dir, '141124_ST-INPROGRESS1_02_AFCIDXX')
        in_progress_done = os.path.join(self.tmp_dir, '141124_ST-INPROGRESSDONE1_02_AFCIDXX')
        completed = os.path.join(self.tmp_dir, '141124_ST-COMPLETED1_01_AFCIDXX')
        dummy = os.path.join(self.tmp_dir, '141124_ST-DUMMY1_01_AFCIDXX')
        complex_run_dir = os.path.join(self.tmp_dir, '141124_ST-COMPLEX1_01_AFCIDXX')
        finished_runs = [to_start, in_progress, in_progress_done, completed]

        # Create runs directory structure
        os.makedirs(self.tmp_dir)
        os.makedirs(running)
        os.makedirs(to_start)
        os.makedirs(os.path.join(in_progress, 'Demultiplexing'))
        os.makedirs(os.path.join(in_progress, 'Demultiplexing_0', 'Reports', 'html', 'FCIDXX', 'all', 'all', 'all'))
        os.makedirs(os.path.join(in_progress, 'Demultiplexing_1'))
        os.makedirs(os.path.join(in_progress, 'Demultiplexing_2'))
        os.makedirs(os.path.join(in_progress, 'Demultiplexing_3'))
        os.makedirs(os.path.join(in_progress_done, 'Demultiplexing'))
        os.makedirs(os.path.join(in_progress_done, 'Demultiplexing_0/Stats'))
        os.makedirs(os.path.join(completed, 'Demultiplexing', 'Stats'))
        os.makedirs(dummy)
        os.makedirs(os.path.join(complex_run_dir, 'Demultiplexing'))
        os.makedirs(os.path.join(complex_run_dir, 'Demultiplexing_0', 'Stats'))
        os.makedirs(os.path.join(complex_run_dir, 'Demultiplexing_1', 'Stats'))
        os.makedirs(os.path.join(complex_run_dir, 'Demultiplexing_0', 'N__One_20_01', 'Sample_P12345_1001'))
        os.makedirs(os.path.join(complex_run_dir,'Demultiplexing_0', 'Reports', 'html','FCIDXX', 'all', 'all', 'all'))
        os.makedirs(os.path.join(complex_run_dir,'Demultiplexing_1', 'Reports', 'html','FCIDXX', 'all', 'all', 'all'))

        # Create files indicating that the run is finished
        for run in finished_runs:
            open(os.path.join(run, 'RTAComplete.txt'), 'w').close()

        # Create sample sheets for running demultiplexing
        open(os.path.join(in_progress, 'SampleSheet_0.csv'), 'w').close()
        open(os.path.join(in_progress, 'SampleSheet_1.csv'), 'w').close()
        open(os.path.join(in_progress, 'SampleSheet_2.csv'), 'w').close()
        open(os.path.join(in_progress, 'SampleSheet_3.csv'), 'w').close()
        open(os.path.join(in_progress_done, 'SampleSheet_0.csv'), 'w').close()
        shutil.copy('data/samplesheet.csv', os.path.join(completed, 'SampleSheet.csv'))
        shutil.copy('data/samplesheet.csv', os.path.join(complex_run_dir, 'SampleSheet_0.csv'))
        shutil.copy('data/samplesheet.csv', os.path.join(complex_run_dir, 'SampleSheet_1.csv'))

        # Create files indicating that demultiplexing is ongoing
        open(os.path.join(in_progress_done, 'Demultiplexing_0', 'Stats', 'DemultiplexingStats.xml'), 'w').close()
        open(os.path.join(in_progress_done, 'Demultiplexing_0', 'Stats', 'DemuxSummaryF1L1.txt'), 'w').close()
        shutil.copy('data/lane.html', os.path.join(in_progress,'Demultiplexing_0', 'Reports', 'html', 'FCIDXX', 'all', 'all', 'all'))

        # Create files indicating that the preprocessing is done
        open(os.path.join(completed, 'Demultiplexing', 'Stats', 'DemultiplexingStats.xml'), 'w').close()
        open(os.path.join(completed, 'Demultiplexing', 'Undetermined_S0_L001_R1_001.fastq.gz'), 'w').close()
        open(os.path.join(complex_run_dir, 'Demultiplexing_0', 'N__One_20_01', 'Sample_P12345_1001', 'P16510_1001_S1_L001_R1_001.fastq.gz'), 'w').close()
        open(os.path.join(complex_run_dir, 'Demultiplexing_0', 'N__One_20_01', 'Sample_P12345_1001', 'P16510_1001_S1_L001_R2_001.fastq.gz'), 'w').close()
        with io.open(os.path.join(completed, 'Demultiplexing', 'Stats', 'Stats.json'), 'w', encoding="utf-8") as stats_json:
            stats_json.write(unicode(json.dumps({'silly': 1}, ensure_ascii=False)))

        # Copy transfer file with the completed run
        shutil.copy('data/test_transfer.tsv', self.transfer_file)

        # Move sample RunInfo.xml file to every run directory
        for run in [running, to_start, in_progress, in_progress_done, completed, dummy, complex_run_dir]:
            shutil.copy('data/RunInfo.xml', run)
            shutil.copy('data/runParameters.xml', run)

        # Create files for complex case
        shutil.copy('data/Stats.json', os.path.join(complex_run_dir, 'Demultiplexing_0', 'Stats', 'Stats.json'))
        shutil.copy('data/Stats.json', os.path.join(complex_run_dir, 'Demultiplexing_1', 'Stats', 'Stats.json'))
        shutil.copy('data/lane.html', os.path.join(complex_run_dir,'Demultiplexing_0', 'Reports', 'html', 'FCIDXX', 'all', 'all', 'all'))
        shutil.copy('data/lane.html', os.path.join(complex_run_dir,'Demultiplexing_1', 'Reports', 'html', 'FCIDXX', 'all', 'all', 'all'))
        shutil.copy('data/laneBarcode.html', os.path.join(complex_run_dir,'Demultiplexing_0', 'Reports', 'html', 'FCIDXX', 'all', 'all', 'all'))
        shutil.copy('data/laneBarcode.html', os.path.join(complex_run_dir,'Demultiplexing_1', 'Reports', 'html', 'FCIDXX', 'all', 'all', 'all'))

        # Create archive dir
        self.archive_dir = os.path.join(self.tmp_dir, 'archive')
        os.makedirs(self.archive_dir)

        # Create run objects
        self.running = HiSeqX_Run(os.path.join(self.tmp_dir,
                                               '141124_ST-RUNNING1_03_AFCIDXX'),
                                  CONFIG['analysis']['HiSeqX'])
        self.to_start = Run(os.path.join(self.tmp_dir,
                                         '141124_ST-TOSTART1_04_FCIDXXX'),
                            CONFIG['analysis']['HiSeqX'])
        self.in_progress = HiSeqX_Run(os.path.join(self.tmp_dir,
                                                   '141124_ST-INPROGRESS1_02_AFCIDXX'),
                                      CONFIG['analysis']['HiSeqX'])
        self.in_progress_done = HiSeqX_Run(os.path.join(self.tmp_dir,
                                                        '141124_ST-INPROGRESSDONE1_02_AFCIDXX'),
                                           CONFIG['analysis']['HiSeqX'])
        self.completed = Run(os.path.join(self.tmp_dir,
                                          '141124_ST-COMPLETED1_01_AFCIDXX'),
                             CONFIG['analysis']['HiSeqX'])
        self.dummy_run = Run(os.path.join(self.tmp_dir,
                                          '141124_ST-DUMMY1_01_AFCIDXX'),
                             CONFIG['analysis']['HiSeq'])
        self.finished_runs = [self.to_start, self.in_progress, self.completed]
        self.complex_run = Run(os.path.join(self.tmp_dir, '141124_ST-COMPLEX1_01_AFCIDXX'),
                               CONFIG['analysis']['HiSeq'])

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.tmp_dir)

    def test_run_setup(self):
        """Raise RuntimeError if files are missing."""
        # if rundir missing
        with self.assertRaises(RuntimeError):
            Run('missing_dir', CONFIG['analysis']['HiSeqX'])
        # if config incomplete
        with self.assertRaises(RuntimeError):
            Run(self.tmp_dir, CONFIG['analysis']['DummySeq'])
        # if runParameters.xml missing
        with self.assertRaises(RuntimeError):
            Run(self.tmp_dir, CONFIG['analysis']['HiSeq'])

    def test_is_sequencing_done(self):
        """Is finished should be True only if "RTAComplete.txt" file is present."""
        self.assertFalse(self.running._is_sequencing_done())
        self.assertTrue(all([run._is_sequencing_done for run in self.finished_runs]))

    def test_get_run_status(self):
        """Get the run status based on present files."""
        self.assertEqual('SEQUENCING', self.running.get_run_status())
        self.assertEqual('TO_START', self.to_start.get_run_status())
        self.assertEqual('IN_PROGRESS', self.in_progress.get_run_status())
        self.assertEqual('COMPLETED', self.completed.get_run_status())

    def test_is_transferred(self):
        """is_transferred should rely on the info in transfer.tsv."""
        os.makedirs(os.path.join(self.tmp_dir, '141124_ST-DUMMY1_01_AFCIDXX', 'transferring'))
        self.assertTrue(self.dummy_run.is_transferred(self.transfer_file))
        self.assertTrue(self.completed.is_transferred(self.transfer_file))
        self.assertFalse(self.running.is_transferred(self.transfer_file))
        self.assertFalse(self.to_start.is_transferred(self.transfer_file))
        self.assertFalse(self.in_progress.is_transferred( self.transfer_file))
        self.assertFalse(self.completed.is_transferred('missing_file'))

    @mock.patch('taca.illumina.HiSeqX_Runs.HiSeqX_Run._aggregate_demux_results')
    def test_check_run_status_done(self, mock_aggregate_demux_results):
        """Recognize if a demultiplexing run is finished or not."""
        self.in_progress.check_run_status()
        mock_aggregate_demux_results.assert_not_called()
        self.in_progress_done.check_run_status()
        mock_aggregate_demux_results.assert_called_once()

    @mock.patch('taca.illumina.Runs.Run.get_run_status')
    def test_check_run_status_completed(self, mock_status):
        """Return None if run is finished."""
        mock_status.return_value = 'COMPLETED'
        self.assertEqual(self.in_progress.check_run_status(), None)

    def test_get_run_type(self):
        """Return runtype if set."""
        self.assertEqual('NGI-RUN', self.running.get_run_type())
        self.to_start.run_type = False
        with self.assertRaises(RuntimeError):
            self.to_start.get_run_type()

    def test_get_demux_folder(self):
        """Return name of demux folder if set."""
        self.assertEqual('Demultiplexing', self.running._get_demux_folder())

    def test_get_samplesheet(self):
        """Return location of sample sheet."""
        self.assertEqual('data/2014/FCIDXX.csv', self.running._get_samplesheet())

    def test_is_demultiplexing_done(self):
        """Return true if Stats.json exists, else false."""
        self.assertFalse(self.in_progress._is_demultiplexing_done())
        self.assertTrue(self.completed._is_demultiplexing_done())

    def test_is_demultiplexing_started(self):
        """Return true if demux folder exists, else false."""
        self.assertTrue(self.in_progress._is_demultiplexing_started())
        self.assertFalse(self.to_start._is_demultiplexing_started())

    def test_generate_per_lane_base_mask(self):
        """Generate base mask."""
        with self.assertRaises(RuntimeError):
            self.dummy_run._generate_per_lane_base_mask()

        shutil.copy('data/samplesheet_dummy_run.csv', os.path.join(self.tmp_dir,'141124_ST-DUMMY1_01_AFCIDXX', 'SampleSheet.csv'))
        self.dummy_run._set_run_parser_obj(CONFIG['analysis']['HiSeq'])
        expected_mask = {'1': {'Y151I7N3I7N3':
                               {'base_mask': ['Y151', 'I7N3', 'I7N3'],
                                'data': [{'index': 'CGCGCAG',
                                          'Lane': '1',
                                          'Sample_ID': 'Sample_P10000_1001',
                                          'Sample_Project': 'A_Test_18_01',
                                          'Sample_Name': 'Sample_P10000_1001',
                                          'index2': 'CTGCGCG'}]},
                               'Y151I7N3N10':
                               {'base_mask': ['Y151', 'I7N3', 'N10'],
                                'data': [{'index': 'AGGTACC',
                                          'Lane': '1',
                                          'Sample_ID': 'Sample_P10000_1005',
                                          'Sample_Project': 'A_Test_18_01',
                                          'Sample_Name': 'Sample_P10000_1005',
                                          'index2': ''}]}}}
        got_mask = self.dummy_run._generate_per_lane_base_mask()
        self.assertEqual(expected_mask, got_mask)

    def test_compute_base_mask(self):
        """Compute Run base mask."""
        runSetup = [{'IsIndexedRead': 'N', 'NumCycles': '151', 'Number': '1'},
                    {'IsIndexedRead': 'Y', 'NumCycles': '8', 'Number': '2'},
                    {'IsIndexedRead': 'Y', 'NumCycles': '8', 'Number': '3'},
                    {'IsIndexedRead': 'N', 'NumCycles': '151', 'Number': '4'}]
        index_size = 7
        dual_index_sample = True
        index2_size = 7
        got_mask = self.dummy_run._compute_base_mask(runSetup, index_size, dual_index_sample, index2_size)
        expected_mask = ['Y151', 'I7N1', 'I7N1', 'Y151']
        self.assertEqual(got_mask, expected_mask)

    @mock.patch('taca.illumina.Runs.misc.call_external_command')
    def test_transfer_run(self, mock_call_external_command):
        """Call external rsync."""
        self.completed.transfer_run(self.transfer_file)
        command_line = ['rsync', '-Lav', '--no-o', '--no-g', '--chmod=g+rw',
                        '--exclude=Demultiplexing_*/*_*',
                        '--include=*/', '--include=*.file',
                        '--exclude=*', '--prune-empty-dirs',
                        os.path.join(self.tmp_dir, '141124_ST-COMPLETED1_01_AFCIDXX'),
                        'None@None:None']
        mock_call_external_command.assert_called_once_with(command_line,
                                                           log_dir=os.path.join(self.tmp_dir, '141124_ST-COMPLETED1_01_AFCIDXX'),
                                                           prefix='',
                                                           with_log_files=True)

    @mock.patch('taca.illumina.Runs.misc.call_external_command')
    def test_transfer_run_error(self, mock_call_external_command):
        """Handle external rsync error."""
        mock_call_external_command.side_effect = subprocess.CalledProcessError(1, 'some error')
        with self.assertRaises(subprocess.CalledProcessError):
            self.completed.transfer_run(self.transfer_file)

    @mock.patch('taca.illumina.Runs.shutil.move')
    def test_archive_run(self, mock_move):
        """Move file to archive."""
        self.completed.archive_run(self.archive_dir)
        mock_move.assert_called_once_with(os.path.join(self.tmp_dir, '141124_ST-COMPLETED1_01_AFCIDXX'),
                                          os.path.join(self.archive_dir, '141124_ST-COMPLETED1_01_AFCIDXX'))

    @mock.patch('taca.illumina.Runs.misc.send_mail')
    def test_send_mail(self, mock_send_mail):
        """Send mail to user."""
        self.completed.send_mail('Hello', 'user@email.com')
        mock_send_mail.assert_called_once_with('141124_ST-COMPLETED1_01_AFCIDXX', 'Hello', 'user@email.com')

    def test_is_unpooled_lane(self):
        """Check if lane is unpooled."""
        self.assertTrue(self.in_progress.is_unpooled_lane('2'))

    def test_get_samples_per_lane(self):
        """Return samples from samplesheet."""
        expected_samples = {'1': 'P10000_1001', '2': 'P10000_1005', '3': 'P10000_1006', '4': 'P10000_1007'}
        got_samples =  self.in_progress.get_samples_per_lane()
        self.assertEqual(expected_samples, got_samples)

    @mock.patch('taca.illumina.Runs.os.rename')
    def test_rename_undet(self, mock_rename):
        """Prepend sample name to file name."""
        samples_per_lane = {'1': 'P10000_1001', '2': 'P10000_1005'}
        lane = '1'
        self.completed._rename_undet(lane, samples_per_lane)
        old_name = os.path.join(self.tmp_dir, '141124_ST-COMPLETED1_01_AFCIDXX', 'Demultiplexing', 'Undetermined_S0_L001_R1_001.fastq.gz')
        new_name = os.path.join(self.tmp_dir, '141124_ST-COMPLETED1_01_AFCIDXX', 'Demultiplexing', 'P10000_1001_Undetermined_L011_R1_001.fastq.gz')
        mock_rename.assert_called_once_with(old_name, new_name)

    @mock.patch('taca.illumina.Runs.os.symlink')
    def test_aggregate_demux_results_simple_complex(self, mock_symlink):
        """Aggregare demux results simple case."""
        simple_lanes = {'141124_ST-INPROGRESSDONE1_02_AFCIDXX': 0}
        complex_lanes = {}
        self.assertTrue(self.in_progress_done._aggregate_demux_results_simple_complex(simple_lanes, complex_lanes))
        calls = [mock.call(os.path.join(self.tmp_dir, '141124_ST-INPROGRESSDONE1_02_AFCIDXX/Demultiplexing_0/Stats/DemultiplexingStats.xml'),
                           os.path.join(self.tmp_dir, '141124_ST-INPROGRESSDONE1_02_AFCIDXX/Demultiplexing/Stats/DemultiplexingStats.xml')),
                 mock.call(os.path.join(self.tmp_dir, '141124_ST-INPROGRESSDONE1_02_AFCIDXX/Demultiplexing_0/Stats/AdapterTrimming.txt'),
                           os.path.join(self.tmp_dir, '141124_ST-INPROGRESSDONE1_02_AFCIDXX/Demultiplexing/Stats/AdapterTrimming.txt')),
                 mock.call(os.path.join(self.tmp_dir, '141124_ST-INPROGRESSDONE1_02_AFCIDXX/Demultiplexing_0/Stats/ConversionStats.xml'),
                           os.path.join(self.tmp_dir, '141124_ST-INPROGRESSDONE1_02_AFCIDXX/Demultiplexing/Stats/ConversionStats.xml')),
                 mock.call(os.path.join(self.tmp_dir, '141124_ST-INPROGRESSDONE1_02_AFCIDXX/Demultiplexing_0/Stats/Stats.json'),
                           os.path.join(self.tmp_dir, '141124_ST-INPROGRESSDONE1_02_AFCIDXX/Demultiplexing/Stats/Stats.json'))]
        mock_symlink.assert_has_calls(calls)

    @mock.patch('taca.illumina.Runs.json.dump')
    def test_aggregate_demux_results_simple_complex_complex(self, mock_json_dump):
        """Aggregare demux results complex case."""
        complex_lanes = {'141124_ST-COMPLEX1_01_AFCIDXX': 0}
        simple_lanes = {}
        self.assertTrue(self.complex_run._aggregate_demux_results_simple_complex(simple_lanes, complex_lanes))
        mock_json_dump.assert_called_once()

    def test_aggregate_demux_results_simple_complex_fail(self):
        """Aggregate_demux_results_simple_complex should raise error if files are missing."""
        complex_lanes = {'1': 0}
        simple_lanes = {}
        with self.assertRaises(RuntimeError):
            self.in_progress_done._aggregate_demux_results_simple_complex(simple_lanes, complex_lanes)

    def test_create_folder_structure(self):
        """Make directory structure."""
        root = self.tmp_dir
        dirs = ['dir1', 'dir2']
        path = _create_folder_structure(root, dirs)
        self.assertEqual(path, os.path.join(self.tmp_dir, 'dir1/dir2'))

    def test_generate_lane_html(self):
        """Generate lane HTML."""
        html_report = 'data/lane.html'
        html_report_lane_parser = LaneBarcodeParser(html_report)
        html_file = os.path.join(self.tmp_dir, 'generated_lane.html')
        expected_file = 'data/lane_result.html'
        _generate_lane_html(html_file, html_report_lane_parser)
        self.assertTrue(filecmp.cmp(html_file, expected_file))


class TestHiSeqRuns(unittest.TestCase):
    """Tests for the HiSeq_Run run class."""
    @classmethod
    def setUpClass(self):
        """ Creates the following directory tree for testing purposes:

        tmp/
        |__ 141124_ST-RUNNING_03_AHISEQFCIDXX
        |   |__ RunInfo.xml
        |__ 141124_ST-TOSTART_04_AHISEQFCIDXX
            |__ RunInfo.xml
            |__ RTAComplete.txt
        """
        self.tmp_dir = os.path.join(tempfile.mkdtemp(), 'tmp')

        running = os.path.join(self.tmp_dir, '141124_ST-RUNNING1_03_AHISEQFCIDXX')
        to_start = os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AHISEQFCIDXX')

        # Create runs directory structure
        os.makedirs(self.tmp_dir)
        os.makedirs(running)
        os.makedirs(to_start)

        # Create files indicating that the run is finished
        open(os.path.join(running, 'RTAComplete.txt'), 'w').close()

        # Move sample RunInfo.xml file to every run directory
        for run in [running, to_start]:
            shutil.copy('data/RunInfo.xml', run)
            shutil.copy('data/runParameters.xml', run)

        # Create run objects
        self.running = HiSeq_Run(os.path.join(self.tmp_dir,
                                               '141124_ST-RUNNING1_03_AHISEQFCIDXX'),
                                  CONFIG['analysis']['HiSeq'])
        self.to_start = HiSeq_Run(os.path.join(self.tmp_dir,
                                         '141124_ST-TOSTART1_04_AHISEQFCIDXX'),
                            CONFIG['analysis']['HiSeq'])

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.tmp_dir)

    def test_copy_samplesheet(self):
        """Copy HiSeq SampleSheet."""
        self.running._copy_samplesheet()
        self.assertTrue(os.path.isfile(os.path.join(self.tmp_dir, '141124_ST-RUNNING1_03_AHISEQFCIDXX', 'SampleSheet.csv')))

    @mock.patch('taca.illumina.HiSeq_Runs.HiSeq_Run._get_samplesheet')
    @mock.patch('taca.illumina.HiSeq_Runs.SampleSheetParser')
    def test_copy_samplesheet_missing(self, mock_parser, mock_samplesheet):
        """Raise RuntimeError if HiSeq samplesheet is missing."""
        mock_samplesheet.return_value = 'some/missing/file.csv'
        with self.assertRaises(RuntimeError):
            self.running._copy_samplesheet()

    def test_generate_clean_samplesheet(self):
        """Make clean HiSeq sample sheet."""
        ssparser = SampleSheetParser('data/samplesheet_dual_index.csv')
        expected_samplesheet = '''[Header]
Date,None
Experiment Name,CIDXX
Investigator Name,Test
[Data]
Lane,Sample_ID,Sample_Name,index,index2,Sample_Project,FCID,SampleRef,Description,Control,Recipe,Operator
1,Sample_Sample_P10000_1001,Sample_P10000_1001,CGCGCAG,CTGCGCG,A_Test_18_01,HISEQFCIDXX,Human (Homo sapiens GRCh37),A_Test_18_01,N,2x50,Some_One
1,Sample_Sample_P10000_1005,Sample_P10000_1005,AGGTACC,,A_Test_18_01,HISEQFCIDXX,Human (Homo sapiens GRCh37),A_Test_18_01,N,2x50,Some_One
'''
        got_samplesheet = self.running._generate_clean_samplesheet(ssparser)
        self.assertEqual(got_samplesheet, expected_samplesheet)

    def test_data_filed_conversion(self):
        """Convert fields in the HiSeq sample sheet."""
        fields_to_convert = ['FCID',
                            'Lane',
                           'SampleID',
                           'SampleRef',
                           'Index',
                           'Description',
                           'Control',
                           'Recipe',
                           'Operator',
                           'SampleProject'
                           ]
        converted_fields = []
        for field in fields_to_convert:
            converted_field = _data_filed_conversion(field)
            converted_fields.append(converted_field)

        expected_fields = ['FCID',
                           'Lane',
                           'Sample_ID',
                           'SampleRef',
                           'index',
                           'Description',
                           'Control',
                           'Recipe',
                           'Operator',
                           'Sample_Project'
                           ]
        self.assertEqual(expected_fields, converted_fields)
        with self.assertRaises(RuntimeError):
            _data_filed_conversion('not_a_field')

    @mock.patch('taca.illumina.HiSeq_Runs.misc.call_external_command_detached')
    def test_demultiplex_run(self, mock_call_external):
        """Demultiplex HiSeq Run."""
        self.to_start.demultiplex_run()
        mock_call_external.assert_called_once_with(['path_to_bcl_to_fastq',
                                                    '--some-opt', 'some_val',
                                                    '--other-opt',
                                                    '--output-dir', 'Demultiplexing_0',
                                                    '--use-bases-mask', '1:Y151,I7N3,N10',
                                                    '--tiles', 's_1',
                                                    '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AHISEQFCIDXX', 'SampleSheet_0.csv')],
                                                   prefix='demux_0',
                                                   with_log_files=True)

    @mock.patch('taca.illumina.HiSeq_Runs.misc.call_external_command_detached')
    @mock.patch('taca.illumina.HiSeq_Runs.HiSeq_Run._generate_per_lane_base_mask')
    def test_demultiplex_run_complex(self, mock_mask, mock_call_external):
        """Demultiplex complex HiSeq Run."""
        mock_mask.return_value = {'1':
                                  {'Y151I7N1Y151':
                                   {'base_mask': ['Y151', 'I7N1', 'Y151'],
                                    'data': [{'Control': 'N',
                                              'Lane': '1',
                                              'Sample_ID': 'Sample_Sample_P10000_1001',
                                              'Sample_Name': 'Sample_P10000_1001',
                                              'index': 'CGCGCAA',
                                              'index2': 'CGCGCAC',
                                              'Sample_Project': 'A_Test_18_01',
                                              'FCID': 'HISEQFCIDXX',
                                              'SampleRef': 'Human (Homo sapiens GRCh37)',
                                              'Description': 'A_Test_18_01',
                                              'Recipe': '2x50',
                                              'Operator': 'Some_One'}]},
                                  'Y150I7N1Y151':
                                   {'base_mask': ['Y150', 'I7N1', 'Y151'],
                                    'data': [{'Control': 'N',
                                              'Lane': '1',
                                              'Sample_ID': 'Sample_Sample_P10000_1001',
                                              'Sample_Name': 'Sample_P10000_1001',
                                              'index': 'CGCGCAG',
                                              'index2': 'CGCGCGG',
                                              'Sample_Project': 'A_Test_18_01',
                                              'FCID': 'HISEQFCIDXX',
                                              'SampleRef': 'Human (Homo sapiens GRCh37)',
                                              'Description': 'A_Test_18_01',
                                              'Recipe': '2x50',
                                              'Operator': 'Some_One'}]}
                                  }}
        self.to_start.demultiplex_run()
        calls_alt_1 = [mock.call(['path_to_bcl_to_fastq',
                                  '--some-opt', 'some_val',
                                  '--other-opt',
                                  '--output-dir', 'Demultiplexing_0',
                                  '--use-bases-mask', '1:Y150,I7N1,Y151',
                                  '--tiles', 's_1',
                                  '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AHISEQFCIDXX', 'SampleSheet_0.csv')],
                                 with_log_files=True, prefix='demux_0'),
                       mock.call(['path_to_bcl_to_fastq',
                                  '--some-opt', 'some_val',
                                  '--other-opt',
                                  '--output-dir', 'Demultiplexing_1',
                                  '--use-bases-mask', '1:Y151,I7N1,Y151',
                                  '--tiles', 's_1',
                                  '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AHISEQFCIDXX', 'SampleSheet_1.csv')],
                                 with_log_files=True, prefix='demux_1')]
        calls_alt_2 = [mock.call(['path_to_bcl_to_fastq',
                                  '--some-opt', 'some_val',
                                  '--other-opt',
                                  '--output-dir', 'Demultiplexing_0',
                                  '--use-bases-mask', '1:Y151,I7N1,Y151',
                                  '--tiles', 's_1',
                                  '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AHISEQFCIDXX', 'SampleSheet_0.csv')],
                                 with_log_files=True, prefix='demux_0'),
                       mock.call(['path_to_bcl_to_fastq',
                                  '--some-opt', 'some_val',
                                  '--other-opt',
                                  '--output-dir', 'Demultiplexing_1',
                                  '--use-bases-mask', '1:Y150,I7N1,Y151',
                                  '--tiles', 's_1',
                                  '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AHISEQFCIDXX', 'SampleSheet_1.csv')],
                                 with_log_files=True, prefix='demux_1')]
        try:
            mock_call_external.assert_has_calls(calls_alt_1)
        except AssertionError as e:
            mock_call_external.assert_has_calls(calls_alt_2)

    def test_generate_bcl2fastq_command(self):
        """Generate command to demultiplex HiSeq."""
        mask = self.to_start._generate_per_lane_base_mask()
        got_command = self.to_start._generate_bcl2fastq_command(mask, True, 0, True)
        expexted_command = ['path_to_bcl_to_fastq',
                            '--some-opt', 'some_val',
                            '--other-opt',
                            '--output-dir', 'Demultiplexing_0',
                            '--use-bases-mask', '1:Y151,I7N3,N10',
                            '--tiles', 's_1',
                            '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AHISEQFCIDXX', 'SampleSheet_0.csv'),
                            '--mask-short-adapter-reads', '0']
        self.assertEqual(got_command, expexted_command)

    @mock.patch('taca.illumina.HiSeq_Runs.HiSeq_Run._aggregate_demux_results_simple_complex')
    def test_aggregate_demux_results(self, mock_aggregate_demux_results_simple_complex):
        """Aggregate the results from different demultiplexing steps HiSeq."""
        self.to_start._aggregate_demux_results()
        mock_aggregate_demux_results_simple_complex.assert_called_with({'1':
                                                                       {'Y151I7N3N10':
                                                                        {'base_mask': ['Y151', 'I7N3', 'N10'],
                                                                         'data': [{'Control': 'N',
                                                                                   'index': 'CGCGCAG',
                                                                                   'Lane': '1',
                                                                                   'Description': 'A_Test_18_01',
                                                                                   'Sample_ID': 'Sample_Sample_P10000_1001',
                                                                                   'Recipe': '2x50',
                                                                                   'FCID': 'HISEQFCIDXX',
                                                                                   'SampleRef': 'Human (Homo sapiens GRCh37)',
                                                                                   'Operator': 'Some_One',
                                                                                   'Sample_Project': 'A_Test_18_01',
                                                                                   'Sample_Name': 'Sample_P10000_1001',
                                                                                   'index2': ''},
                                                                                  {'Control': 'N',
                                                                                   'index': 'AGGTACC',
                                                                                   'Lane': '1',
                                                                                   'Description': 'A_Test_18_01',
                                                                                   'Sample_ID': 'Sample_Sample_P10000_1005',
                                                                                   'Recipe': '2x50',
                                                                                   'FCID': 'HISEQFCIDXX',
                                                                                   'SampleRef': 'Human (Homo sapiens GRCh37)',
                                                                                   'Operator': 'Some_One',
                                                                                   'Sample_Project': 'A_Test_18_01',
                                                                                   'Sample_Name': 'Sample_P10000_1005',
                                                                                   'index2': ''}]
                                                                        }
                                                                       }}, {})

    @mock.patch('taca.illumina.HiSeq_Runs.HiSeq_Run._aggregate_demux_results_simple_complex')
    @mock.patch('taca.illumina.HiSeq_Runs.HiSeq_Run._generate_per_lane_base_mask')
    def test_aggregate_demux_results_complex(self, mock_base_mask, mock_aggregate_demux_results_simple_complex):
        """Aggregate the results from different demultiplexing steps HiSeq, complex case."""
        mock_base_mask.return_value = {'1':
                                  {'Y151I7N1Y151':
                                   {'base_mask': ['Y151', 'I7N1', 'Y151'],
                                    'data': []},
                                  'Y150I7N1Y151':
                                   {'base_mask': ['Y150', 'I7N1', 'Y151'],
                                    'data': []}
                                  }}
        self.to_start._aggregate_demux_results()
        mock_aggregate_demux_results_simple_complex.assert_called_once_with({}, {'1':
                                                                       {'Y151I7N1Y151':
                                                                        {'base_mask': ['Y151', 'I7N1', 'Y151'],
                                                                         'data': []},
                                                                        'Y150I7N1Y151':
                                                                        {'base_mask': ['Y150', 'I7N1', 'Y151'],
                                                                         'data': []}
                                                                       }})

class TestHiSeqXRuns(unittest.TestCase):
    """Tests for the HiSeqX_Run run class."""
    @classmethod
    def setUpClass(self):
        """ Creates the following directory tree for testing purposes:

        tmp/
        |__ 141124_ST-RUNNING_03_AFCIDXX
        |   |__ RunInfo.xml
        |__ 141124_ST-TOSTART_04_AFCIDXX
            |__ RunInfo.xml
            |__ RTAComplete.txt
        """
        self.tmp_dir = os.path.join(tempfile.mkdtemp(), 'tmp')

        running = os.path.join(self.tmp_dir, '141124_ST-RUNNING1_03_AFCIDXX')
        to_start = os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AFCIDXX')

        # Create runs directory structure
        os.makedirs(self.tmp_dir)
        os.makedirs(running)
        os.makedirs(to_start)

        # Create files indicating that the run is finished
        open(os.path.join(running, 'RTAComplete.txt'), 'w').close()

        # Move sample RunInfo.xml file to every run directory
        for run in [running, to_start]:
            shutil.copy('data/RunInfo.xml', run)
            shutil.copy('data/runParameters.xml', run)

        # Create run objects
        self.running = HiSeqX_Run(os.path.join(self.tmp_dir,
                                               '141124_ST-RUNNING1_03_AFCIDXX'),
                                  CONFIG["analysis"]["HiSeqX"])
        self.to_start = HiSeqX_Run(os.path.join(self.tmp_dir,
                                                '141124_ST-TOSTART1_04_AFCIDXX'),
                                   CONFIG["analysis"]["HiSeqX"])
    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.tmp_dir)

    def test_copy_samplesheet(self):
        """Copy HiSeqX SampleSheet."""
        os.remove(os.path.join(self.tmp_dir, '141124_ST-RUNNING1_03_AFCIDXX', 'SampleSheet.csv'))
        self.running._copy_samplesheet()
        self.assertTrue(os.path.isfile(os.path.join(self.tmp_dir, '141124_ST-RUNNING1_03_AFCIDXX', 'SampleSheet.csv')))

    def test_generate_clean_samplesheet(self):
        """Make clean HiSeqX sample sheet."""
        ssparser = SampleSheetParser('data/2014/FCIDXX.csv')
        indexfile = dict()
        indexfile['tenX'] = 'data/test_10X_indexes'
        indexfile['smartseq'] = 'data/test_smartseq_indexes'
        expected_samplesheet = u'''[Header]
Date,None
Experiment Name,CIDXX
Investigator Name,Test
[Data]
Lane,Sample_ID,Sample_Name,Sample_Plate,Sample_Well,index,index2,Project,Description
1,Sample_P10000_1001,P10000_1001,CIDXX,1:1,AACCGTAA,,A_Test_18_01,
1,Sample_P10000_1001,P10000_1001,CIDXX,1:1,GGTTTACT,,A_Test_18_01,
1,Sample_P10000_1001,P10000_1001,CIDXX,1:1,CTAAACGG,,A_Test_18_01,
1,Sample_P10000_1001,P10000_1001,CIDXX,1:1,TCGGCGTC,,A_Test_18_01,
2,Sample_P10000_1005,P10000_1005,CIDXX,2:1,AGGTACC,,A_Test_18_01,
3,Sample_P10000_1006,P10000_1006,CIDXX,3:1,TGTATCCGAA,CACAGGTGAA,A_Test_18_01,
3,Sample_P10000_1006,P10000_1006,CIDXX,3:1,GAGCGCCTAT,TTGGTACGCG,A_Test_18_01,
3,Sample_P10000_1006,P10000_1006,CIDXX,3:1,TAAGACGGTG,TTGGTACGCG,A_Test_18_01,
3,Sample_P10000_1006,P10000_1006,CIDXX,3:1,GCTAGGTCAA,CACAGGTGAA,A_Test_18_01,
4,Sample_P10000_1007,P10000_1007,CIDXX,4:1,GTAACATGCG,AGTGTTACCT,A_Test_18_01,
'''
        got_samplesheet = _generate_clean_samplesheet(ssparser, indexfile, rename_samples=True, rename_qPCR_suffix = True, fields_qPCR=[ssparser.dfield_snm])
        self.assertEqual(got_samplesheet, expected_samplesheet)

    @mock.patch('taca.illumina.HiSeqX_Runs.misc.call_external_command_detached')
    def test_demultiplex_run(self, mock_call_external):
        """Demultiplex HiSeqX Run."""
        self.to_start.demultiplex_run()
        calls = [mock.call(['path_to_bcl_to_fastq',
                            '--output-dir', 'Demultiplexing_0',
                            '--opt', 'b',
                            '--c', '--a',
                            '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AFCIDXX/SampleSheet_0.csv'),
                            '--use-bases-mask', '1:Y151,I8N2,N10'],
                           prefix='demux_0', with_log_files=True),
                 mock.call(['path_to_bcl_to_fastq',
                            '--output-dir', 'Demultiplexing_1',
                            '--opt', 'b',
                            '--c',
                            '--e',
                            '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AFCIDXX/SampleSheet_1.csv'),
                            '--use-bases-mask', '4:Y151,I10,I10'],
                           prefix='demux_1', with_log_files=True),
                 mock.call(['path_to_bcl_to_fastq',
                            '--output-dir', 'Demultiplexing_2',
                            '--opt', 'b',
                            '--c',
                            '--d',
                            '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AFCIDXX/SampleSheet_2.csv'),
                            '--use-bases-mask', '3:Y151,I10,I10'],
                           prefix='demux_2', with_log_files=True),
                 mock.call(['path_to_bcl_to_fastq',
                            '--output-dir', 'Demultiplexing_3',
                            '--opt', 'b',
                            '--c',
                            '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AFCIDXX/SampleSheet_3.csv'),
                            '--use-bases-mask', '2:Y151,I7N3,N10'],
                           prefix='demux_3', with_log_files=True)]

        mock_call_external.assert_has_calls(calls)

    @mock.patch('taca.illumina.HiSeqX_Runs.HiSeqX_Run._aggregate_demux_results_simple_complex')
    def test_aggregate_demux_results(self, mockaggregate_demux_results_simple_complex):
        """Aggregate the results from different demultiplexing steps HiSeqX."""
        self.to_start._aggregate_demux_results()
        mockaggregate_demux_results_simple_complex.assert_called_with({'1': 0, '3': 0, '2': 0, '4': 0}, {})

    def test_generate_bcl_command(self):
        """Generate bcl command HiSeqX."""
        sample_type = '10X_GENO'
        mask_table = {'1': [7, 0], '2': [7, 0]}
        expected_command = ['path_to_bcl_to_fastq',
                            '--output-dir', 'Demultiplexing_0',
                            '--opt', 'b',
                            '--c',
                            '--a',
                            '--sample-sheet', os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AFCIDXX/SampleSheet_0.csv'),
                            '--use-bases-mask', '1:Y151,I7N3,N10',
                            '--use-bases-mask', '2:Y151,I7N3,N10']
        got_command = self.to_start.generate_bcl_command(sample_type, mask_table, 0)
        self.assertEqual(expected_command, got_command)

    def test_generate_per_lane_base_mask(self):
        """Generate base mask HiSeqX."""
        sample_type = 'ordinary'
        mask_table = {'1': [7, 0], '2': [7, 0]}
        got_mask = self.to_start._generate_per_lane_base_mask(sample_type, mask_table)
        expected_mask = {'1':
                         {'Y151I7N3N10':
                          {'base_mask': ['Y151', 'I7N3', 'N10']}},
                         '2':
                         {'Y151I7N3N10':
                          {'base_mask': ['Y151', 'I7N3', 'N10']}}}
        self.assertEqual(got_mask, expected_mask)

    def test_compute_base_mask(self):
        """Compute base mask HiSeqX."""
        runSetup = self.to_start.runParserObj.runinfo.get_read_configuration()
        sample_type = 'ordinary'
        index1_size = 7
        is_dual_index = True
        index2_size = 0
        got_mask = self.to_start._compute_base_mask(runSetup, sample_type, index1_size, is_dual_index, index2_size)
        expected_mask = ['Y151', 'I7N3', 'N10']
        self.assertEqual(got_mask, expected_mask)

    def test_classify_samples(self):
        """Classify HiSeqX samples."""
        indexfile = dict()
        indexfile['tenX'] = 'data/test_10X_indexes'
        indexfile['smartseq'] = 'data/test_smartseq_indexes'
        got_sample_table = _classify_samples(indexfile, SampleSheetParser('data/samplesheet_sample_check.csv'))
        expected_sample_table = {'1': [('P10000_1001',
                                       {'sample_type': '10X_GENO',
                                        'index_length': [8, 0]})],
                                '3': [('P10000_1001',
                                       {'sample_type': '10X_ATAC',
                                        'index_length': [8, 16]})],
                                '2': [('P10000_1005',
                                       {'sample_type': 'ordinary',
                                        'index_length': [7, 0]})],
                                '5': [('P10000_1005',
                                       {'sample_type': 'ordinary',
                                        'index_length': [0, 0]})],
                                '4': [('P10000_1005',
                                       {'sample_type': 'IDT_UMI',
                                        'index_length': [4, 0]})],
                                '6': [('P10000_1006',
                                       {'sample_type': 'SMARTSEQ',
                                        'index_length': [10, 10]})],
                                '7': [('P10000_1007',
                                       {'sample_type': '10X_ST',
                                        'index_length': [10, 10]})]}
        self.assertEqual(got_sample_table, expected_sample_table)

    def test_parse_10X_indexes(self):
        """Parse 10X indexes HiSeqX."""
        got_index_dict = parse_10X_indexes('data/test_10X_indexes')
        expected_index_dict = {'SI-GA-A1':
                               ['GGTTTACT', 'CTAAACGG', 'TCGGCGTC', 'AACCGTAA'],
                               'SI-NA-A1':
                               ['AAACGGCG', 'CCTACCAT', 'GGCGTTTC', 'TTGTAAGA'],
                               'SI-GA-A2':
                               ['TTTCATGA', 'ACGTCCCT', 'CGCATGTG', 'GAAGGAAC'],
                               'SI-TT-A1':
                               ['GTAACATGCG', 'AGTGTTACCT']}
        self.assertEqual(got_index_dict, expected_index_dict)

    def test_parse_smartseq_indexes(self):
        """Parse SmartSeq indexes HiSeqX."""
        got_index_dict = parse_smartseq_indexes('data/test_smartseq_indexes')
        expected_index_dict = {'1A':
                               [('GAGCGCCTAT', 'TTGGTACGCG'), ('TAAGACGGTG', 'TTGGTACGCG'), ('GCTAGGTCAA', 'CACAGGTGAA'), ('TGTATCCGAA', 'CACAGGTGAA')],
                               '1B':
                               [('TGAGGTTGTA', 'TTGGTACGCG'), ('CGGTTGAACG', 'TTGGTACGCG'), ('CGGAATCCAA', 'CACAGGTGAA'), ('CGGTAACGGT', 'CACAGGTGAA')],
                               '1C':
                               [('TCCGATAACT', 'TTGGTACGCG'), ('TTCACCACGG', 'TTGGTACGCG'), ('GCACGGTACA', 'CACAGGTGAA'), ('TCTATAGCGG', 'CACAGGTGAA')],
                               '1D':
                               [('GGAAGCTCCT', 'TTGGTACGCG'), ('TACTTGTGCA', 'TTGGTACGCG'), ('TGTAACGAAG', 'CACAGGTGAA'), ('TTGTAATGCG', 'CACAGGTGAA')]}
        self.assertEqual(got_index_dict, expected_index_dict)

    def test_generate_samplesheet_subset(self):
        """Make HiSeqX samplesheet subset."""
        ssparser = SampleSheetParser('data/2014/FCIDXX.csv')
        samples_to_include = {'1': ['P10000_1001']}
        got_data = _generate_samplesheet_subset(ssparser, samples_to_include)
        expected_data = '''[Header]
Date,None
Experiment Name,CIDXX
Investigator Name,Test
[Data]
Lane,Sample_ID,Sample_Name,Sample_Plate,Sample_Well,index,index2,Project,Description
1,Sample_P10000_1001,P10000_1001,CIDXX,1:1,SI-GA-A1,,A_Test_18_01,
'''
        self.assertEqual(got_data, expected_data)


class TestMiSeqRuns(unittest.TestCase):
    """Tests for the MiSeq_Run run class."""
    @classmethod
    def setUpClass(self):
        """Creates the following directory tree for testing purposes:

        tmp/
        |__ 141124_ST-RUNNING_03_AMISEQFCIDXX
        |   |__ RunInfo.xml
        |__ 141124_ST-TOSTART_04_AMISEQFCIDXX
            |__Data/Intensities/BaseCalls
            |                   |__SampleSheet.csv
            |__ RunInfo.xml
            |__ RTAComplete.txt
        """
        self.tmp_dir = os.path.join(tempfile.mkdtemp(), 'tmp')

        running = os.path.join(self.tmp_dir, '141124_ST-RUNNING1_03_AMISEQFCIDXX')
        to_start = os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AMISEQFCIDXX')

        # Create runs directory structure
        os.makedirs(self.tmp_dir)
        os.makedirs(running)
        os.makedirs(to_start)
        os.makedirs(os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AMISEQFCIDXX', 'Data', 'Intensities', 'BaseCalls'))

        sample_sheet_dest = os.path.join(self.tmp_dir, '141124_ST-TOSTART1_04_AMISEQFCIDXX', 'Data', 'Intensities', 'BaseCalls','SampleSheet.csv')
        shutil.copy('data/miseq_test_samplesheet.csv', sample_sheet_dest)

        # Create files indicating that the run is finished
        open(os.path.join(running, 'RTAComplete.txt'), 'w').close()

        # Move sample RunInfo.xml file to every run directory
        for run in [running, to_start]:
            shutil.copy('data/RunInfo.xml', run)
            shutil.copy('data/runParameters.xml', run)

        # Create run objects
        self.running = MiSeq_Run(os.path.join(self.tmp_dir,
                                              '141124_ST-RUNNING1_03_AMISEQFCIDXX'),
                                 CONFIG['analysis']['MiSeq'])
        self.to_start = MiSeq_Run(os.path.join(self.tmp_dir,
                                                '141124_ST-TOSTART1_04_AMISEQFCIDXX'),
                                   CONFIG['analysis']['MiSeq'])

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.tmp_dir)

    def test_generate_clean_samplesheet(self):
        """Make clean MiSeq sample sheet."""
        ssparser = SampleSheetParser('data/2014/MISEQFCIDXX.csv')
        expected_samplesheet = '''[Header]
Assay,null
Chemistry,amplicon
Date,2019-01-23
Description,Production
Experiment Name,A_Test_18_01
Investigator Name,Test
Project Name,A_Test_18_01
Workflow,LibraryQC
[Data]
Lane,Sample_ID,Sample_Name,index,Sample_Project,I7_Index_ID,index2,I5_Index_ID,Sample_Plate,Sample_Well,Description,GenomeFolder
1,Sample_Sample_P10000_1001,Sample_P10000_1001,TATAGCCT,A_Test_18_01,TATAGCCT,GCCTCTAT,GCCTCTAT,P10000P1-A1,A1,Production,/hg19/Sequence/Chromosomes
1,Sample_Sample_P10000_1005,Sample_P10000_1005,TATAGCCT,A_Test_18_01,TATAGCCT,GCGCGAGA,GCGCGAGA,P10000P1-A1,A1,Production,/hg19/Sequence/Chromosomes
'''
        got_samplesheet = self.running._generate_clean_samplesheet(ssparser)
        self.assertEqual(got_samplesheet, expected_samplesheet)

    def test_set_run_type(self):
        """Set MiSeq runtype."""
        run_type = self.to_start.run_type
        self.assertEqual(run_type, 'NGI-RUN')

    def test_get_samplesheet(self):
        """Get sample sheet location MiSeq or return None."""
        found_sample_sheet = self.to_start._get_samplesheet()
        expected_sample_sheet = os.path.join(self.tmp_dir,'141124_ST-TOSTART1_04_AMISEQFCIDXX/Data/Intensities/BaseCalls/SampleSheet.csv')
        self.assertEqual(found_sample_sheet, expected_sample_sheet)
        missing_sample_sheet = self.running._get_samplesheet()
        self.assertIsNone(missing_sample_sheet)

class TestNovaSeqRuns(unittest.TestCase):
    """Tests for the NovaSeq_Run run class."""
    @classmethod
    def setUpClass(self):
        """Creates the following directory tree for testing purposes:

        tmp/
        |__ 141124_ST-RUNNING1_03_AFCIDXX
            |__ RunInfo.xml
        """
        self.tmp_dir = os.path.join(tempfile.mkdtemp(), 'tmp')

        running = os.path.join(self.tmp_dir, '141124_ST-RUNNING1_03_AFCIDXX')
        os.makedirs(self.tmp_dir)
        os.makedirs(running)

        # Create files indicating that the run is finished
        open(os.path.join(running, 'RTAComplete.txt'), 'w').close()

        # Move sample RunInfo.xml file to run directory
        shutil.copy('data/RunInfo.xml', running)
        shutil.copy('data/runParameters.xml', running)

        # Create run objects
        self.running = NovaSeq_Run(os.path.join(self.tmp_dir,
                                              '141124_ST-RUNNING1_03_AFCIDXX'),
                                 CONFIG['analysis']['HiSeqX'])

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.tmp_dir)

    def test_novaseq(self):
        """Set sequencer and run type NovaSeq."""
        self.assertEqual(self.running.sequencer_type, 'NovaSeq')
        self.assertEqual(self.running.run_type, 'NGI-RUN')


class TestNextSeqRuns(unittest.TestCase):
    """Tests for the NextSeq_Run run class."""
    @classmethod
    def setUpClass(self):
        """Creates the following directory tree for testing purposes:

        tmp/
        |__ 141124_ST-RUNNING1_03_AFCIDXX
            |__ RunInfo.xml
        """
        self.tmp_dir = os.path.join(tempfile.mkdtemp(), 'tmp')

        running = os.path.join(self.tmp_dir, '141124_ST-RUNNING1_03_AFCIDXX')
        os.makedirs(self.tmp_dir)
        os.makedirs(running)

        # Create files indicating that the run is finished
        open(os.path.join(running, 'RTAComplete.txt'), 'w').close()

        # Move sample RunInfo.xml file to run directory
        shutil.copy('data/RunInfo.xml', running)
        shutil.copy('data/runParameters.xml', running)

        # Create run objects
        self.running = NextSeq_Run(os.path.join(self.tmp_dir,
                                              '141124_ST-RUNNING1_03_AFCIDXX'),
                                 CONFIG['analysis']['HiSeqX'])

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.tmp_dir)

    def test_nextseq(self):
        """Set sequencer and run type NextSeq."""
        self.assertEqual(self.running.sequencer_type, 'NextSeq')
        self.assertEqual(self.running.run_type, 'NGI-RUN')

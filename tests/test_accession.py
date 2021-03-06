import patsy.database
from patsy.accession import AccessionCsvLoader
from patsy.model import Base
import unittest
from patsy.model import Accession
from .utils import create_test_engine

Session = patsy.database.Session


class TestAccession(unittest.TestCase):
    def setUp(self):
        create_test_engine()
        engine = Session().get_bind()
        Base.metadata.create_all(engine)

    def test_load_single_file(self):
        accession_file = 'tests/data/accessions/sample_accession_1.csv'

        accession_loader = AccessionCsvLoader()
        result = accession_loader.load_from_file(accession_file)

        self.assertEqual(5, result.num_processed)
        self.assertEqual(5, len(result.successes))
        self.assertEqual(0, len(result.failures))

        session = Session()
        num_rows = session.query(Accession).count()
        self.assertEqual(5, num_rows)

    def test_loading_same_file_multiple_times(self):
        accession_file = 'tests/data/accessions/sample_accession_1.csv'

        accession_loader = AccessionCsvLoader()
        result = accession_loader.load_from_file(accession_file)
        self.assertEqual(5, result.num_processed)
        self.assertEqual(5, len(result.successes))
        self.assertEqual(0, len(result.failures))

        accession_loader = AccessionCsvLoader()
        result = accession_loader.load_from_file(accession_file)
        self.assertEqual(5, result.num_processed)
        self.assertEqual(0, len(result.successes))
        self.assertEqual(5, len(result.failures))

        session = Session()
        num_rows = session.query(Accession).count()
        self.assertEqual(5, num_rows)

    def test_load_multiple_files(self):
        accession_dir = 'tests/data/accessions'

        accession_loader = AccessionCsvLoader()
        result = accession_loader.load(accession_dir)

        self.assertEqual(2, result.files_processed)
        self.assertEqual(10, result.total_rows_processed)
        self.assertEqual(10, result.total_successful_rows)
        self.assertEqual(0, result.total_failed_rows)
        self.assertEqual(2, len(result.file_load_results_map.keys()))

        session = Session()
        num_rows = session.query(Accession).count()
        self.assertEqual(10, num_rows)

    def test_csv_to_accession(self):
        # Row with all the elements
        row = dict(batch='Batch1', bytes=123, filename='test_file', md5='ABC123', relpath='test_path/test_file',
                   sourcefile='sourcefile.csv', sourceline=1, timestamp='1/1/2020 12:30pm')

        accession_loader = AccessionCsvLoader()
        accession = accession_loader.csv_to_object(row)
        self.assertEqual(row['batch'], accession.batch)
        self.assertEqual(row['bytes'], accession.bytes)
        self.assertEqual(row['filename'], accession.filename)
        self.assertEqual(row['md5'], accession.md5)
        self.assertEqual(row['relpath'], accession.relpath)
        self.assertEqual(row['sourcefile'], accession.sourcefile)
        self.assertEqual(row['sourceline'], accession.sourceline)
        self.assertEqual(row['timestamp'], accession.timestamp)

        # Rows with missing elements throws exception
        row = dict(batch='Batch1', timestamp='1/1/2020 12:30pm')
        with self.assertRaises(KeyError):
            accession = accession_loader.csv_to_object(row)


#
# import_text_test.py
# Francois-Michel L Heureux, 2016-06-21
# This file is part of MLDB. Copyright 2016 Datacratic. All rights reserved.
#
import tempfile

if False:
    mldb_wrapper = None
mldb = mldb_wrapper.wrap(mldb)  # noqa

class ImportTextTest(MldbUnitTest):

    @classmethod
    def setUpClass(cls):
        cls.regular_lines_file = \
            tempfile.NamedTemporaryFile(dir='build/x86_64/tmp')
        cls.regular_lines_file.write("a,b,c\n")
        cls.regular_lines_file.write("d,e,f\n")
        cls.regular_lines_file.flush()

        cls.irregular_lines_file = \
            tempfile.NamedTemporaryFile(dir='build/x86_64/tmp')
        cls.irregular_lines_file.write("a,b,c\n")
        cls.irregular_lines_file.write("d,e\n")
        cls.irregular_lines_file.write("f,g,h,i\n")
        cls.irregular_lines_file.flush()

    def test_base(self):
        mldb.post('/v1/procedures', {
            'type' : 'import.text',
            'params' : {
                'runOnCreation' : True,
                'dataFileUrl' : 'file://' + self.regular_lines_file.name,
                'outputDataset' : {
                    'id' : 'base_ds',
                    'type' : 'tabular'
                }
            }
        })
        res = mldb.query("SELECT a, b, c FROM base_ds")
        self.assertTableResultEquals(res, [
            ['_rowName', 'a', 'b', 'c'],
            ['2', 'd', 'e', 'f']
        ])

    def test_gen_headers(self):
        """
        MLDB-1741
        """
        mldb.post('/v1/procedures', {
            'type' : 'import.text',
            'params' : {
                'runOnCreation' : True,
                'dataFileUrl' : 'file://' + self.regular_lines_file.name,
                'autoGenerateHeaders' : True,
                'outputDataset' : {
                    'id' : 'gen_headers_ds',
                    'type' : 'tabular'
                }
            }
        })
        res = mldb.query("SELECT * FROM gen_headers_ds")
        self.assertTableResultEquals(res, [
            ['_rowName', '0', '1', '2'],
            ['1', 'a', 'b', 'c'],
            ['2', 'd', 'e', 'f']
        ])

    def test_conflicting_header_config(self):
        msg = "autoGenerateHeaders cannot be true if headers is defined."
        with self.assertRaisesRegexp(mldb_wrapper.ResponseException, msg):
            mldb.post('/v1/procedures', {
                'type' : 'import.text',
                'params' : {
                    'runOnCreation' : True,
                    'dataFileUrl' : 'file://' + self.regular_lines_file.name,
                    'autoGenerateHeaders' : True,
                    'headers' : ['colA', 'colB', 'colC'],
                    'outputDataset' : {
                        'id' : 'gen_headers_ds',
                        'type' : 'tabular'
                    }
                }
            })

    def test_basea_irregular(self):
        msg = "Error parsing CSV row: too many columns in row"
        with self.assertRaisesRegexp(mldb_wrapper.ResponseException, msg):
            mldb.post('/v1/procedures', {
                'type' : 'import.text',
                'params' : {
                    'runOnCreation' : True,
                    'dataFileUrl' : 'file://' + self.irregular_lines_file.name,
                    'outputDataset' : {
                        'id' : 'base_ds',
                        'type' : 'tabular'
                    }
                }
            })

    def test_gen_headers_irregular(self):
        msg = "Error parsing CSV row: too many columns in row"
        with self.assertRaisesRegexp(mldb_wrapper.ResponseException, msg):
            mldb.post('/v1/procedures', {
                'type' : 'import.text',
                'params' : {
                    'runOnCreation' : True,
                    'dataFileUrl' : 'file://' + self.irregular_lines_file.name,
                    'autoGenerateHeaders' : True,
                    'outputDataset' : {
                        'id' : 'base_ds',
                        'type' : 'tabular'
                    }
                }
            })



if __name__ == '__main__':
    mldb.run_tests()

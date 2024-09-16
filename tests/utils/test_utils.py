from backend import utils

class TestUtils:
    def test_get_unique_files(self):
        example_folder = [{'Key': 'test'},
                       {'Key': 'test2'},
                       {'Key': 'test3'},
                       {'Key': 'test'},
                       {'Key': 'test3'},
                       ]
        expected_result = [{'Key': 'test'},
                           {'Key': 'test2'},
                           {'Key': 'test3'}
                           ]

        res = utils.get_unique_files(example_folder)

        assert res == expected_result

    def test_has_substring_in_strings(self):
        example_strings = [
            '/folder/subfolder/subsubfolder/',
            '/newfolder/',
            '/newfolder2/subsubfolder/',
            '/dir/sub/subdir/',
        ]

        example_substring = '/subfolder/subsubfolder/'

        expected_result = True

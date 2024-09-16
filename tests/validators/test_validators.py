import pytest
from backend.s3.validators import PathValidator


class TestPathValidators:
    tests_valid_path = (
        '/',
        '/dir/',
        '/dir/sub_dir/',
        '/d/d/d/d/d/d/'
    )

    tests_invalid_path = (
        '//',
        '/dir//subdir/',
        'dir/',
    )

    validator = PathValidator

    def test_valid_path(self):
        for path in self.tests_valid_path:
            assert self.validator(path).validate()

    def test_invalid_path(self):
        for path in self.tests_invalid_path:
            with pytest.raises(Exception):
                self.validator(path).validate()
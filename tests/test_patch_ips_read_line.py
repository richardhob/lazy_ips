
import unittest.mock

import pytest

import lazy_ips.patch.ips as ips_patch

@pytest.fixture(scope="function")
def fake_file():
    fake = unittest.mock.MagicMock()
    return fake

RECORD_DATA = [
        # offset, size, data
        (1, 1, 2),
        (10, 5, 99),
        (0xffffff, 9, 0xff),
        ]

@pytest.mark.parametrize("offset,size,data", RECORD_DATA)
def test_read_patch_line_record(fake_file, offset, size, data):
    calls = 0
    def _valid(bytes_to_read):
        nonlocal calls

        if calls == 0:
            assert bytes_to_read == 3
            calls += 1
            return int(offset).to_bytes(3, 'big')
        if calls == 1:
            assert bytes_to_read == 2
            calls += 1
            return int(size).to_bytes(2, 'big')
        if calls == 2:
            assert bytes_to_read == size
            calls += 1
            return int(data).to_bytes(size, 'big')
        
    fake_file.read.side_effect = _valid
    line = ips_patch.read_patch_line(fake_file)

    assert line.offset == offset
    assert line.data   == int(data).to_bytes(size, 'big')

@pytest.mark.parametrize("offset,size,data", RECORD_DATA)
def test_read_patch_line_rls(fake_file, offset, size, data):
    calls = 0
    def _valid(bytes_to_read):
        nonlocal calls

        if calls == 0:
            assert bytes_to_read == 3
            calls += 1
            return int(offset).to_bytes(3, 'big')
        if calls == 1:
            assert bytes_to_read == 2
            calls += 1
            return int(0).to_bytes(2, 'big')
        if calls == 2:
            assert bytes_to_read == 2
            calls += 1
            return int(size).to_bytes(2, 'big')
        if calls == 3:
            assert bytes_to_read == 1
            calls += 1
            return int(data).to_bytes(1, 'big') 
        
    fake_file.read.side_effect = _valid
    line = ips_patch.read_patch_line(fake_file)

    assert line.offset == offset
    assert line.data == int(data).to_bytes(1, 'big') * size

def test_read_patch_line_eof(fake_file):
    fake_file.read.return_value = b'EOF'

    line = ips_patch.read_patch_line(fake_file)
    assert line == None

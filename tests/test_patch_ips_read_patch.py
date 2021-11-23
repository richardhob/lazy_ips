import unittest.mock

import pytest

import lazy_ips.patch.ips as patch_ips

@pytest.fixture(scope="function")
def fake_file():
    some_file = unittest.mock.MagicMock()
    return some_file

def test_read_patch_ok(fake_file):
    calls = 0
    def _read(number_of_bytes):
        nonlocal calls

        if calls == 0:
            calls += 1
            assert number_of_bytes == 5
            return b'PATCH'
        if calls == 1:
            calls += 1
            assert number_of_bytes == 3
            return int(1).to_bytes(3, 'big')
        if calls == 2:
            calls += 1
            assert number_of_bytes == 2
            return int(2).to_bytes(2, 'big')
        if calls == 3:
            calls += 1
            assert number_of_bytes == 2
            return int(3).to_bytes(2, 'big')
        if calls == 4:
            calls += 1
            assert number_of_bytes == 3
            return b'EOF'

    fake_file.read.side_effect = _read
    gen = patch_ips.read_patch(fake_file)
    x = [line for line in gen]

    data = x[0]

    assert data.offset == 1
    assert data.data == int(3).to_bytes(2, 'big')

def test_read_patch_bad_header(fake_file):
    calls = 0
    def _read(number_of_bytes):
        nonlocal calls

        if calls == 0:
            calls += 1
            assert number_of_bytes == 5
            return b'PaTCH'
        if calls == 1:
            calls += 1
            assert number_of_bytes == 3
            return b'EOF'

    fake_file.read.side_effect = _read
    gen = patch_ips.read_patch(fake_file)

    with pytest.raises(IOError):
        x = [line for line in gen]

def test_read_patch_bad_header2(fake_file):
    calls = 0
    def _read(number_of_bytes):
        nonlocal calls

        if calls == 0:
            calls += 1
            assert number_of_bytes == 5
            return b'PATC'
        if calls == 1:
            calls += 1
            assert number_of_bytes == 3
            return b'EOF'

    fake_file.read.side_effect = _read
    gen = patch_ips.read_patch(fake_file)

    with pytest.raises(IOError):
        x = [line for line in gen]

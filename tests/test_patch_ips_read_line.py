
import unittest.mock

import pytest

import lazy_ips.patch.ips as ips_patch

@pytest.fixture(scope="session")
def fake_file():
    fake = unittest.mock.MagicMock()
    return fake

def test_read_patch_line_record(fake_file):
    calls = 0
    def _valid(offset):
        nonlocal calls

        # offset, size, data
        if calls == 0:
            calls += 1
            return bytes([0, 0, 1])
        if calls == 1:
            calls += 1
            return bytes([0, 1])
        if calls == 2:
            calls += 1
            return bytes([2])
        
    fake_file.read.side_effect = _valid
    line = ips_patch.read_patch_line(fake_file)

    assert line.offset == 1
    assert line.data == bytes([2])

def test_read_patch_line_rls(fake_file):
    calls = 0
    def _valid(offset):
        nonlocal calls

        # offset, size, data
        if calls == 0:
            calls += 1
            return bytes([0, 0, 1])
        if calls == 1:
            calls += 1
            return bytes([0, 0])
        if calls == 2:
            calls += 1
            return bytes([0, 2])
        if calls == 3:
            calls += 1
            return bytes([2])
        
    fake_file.read.side_effect = _valid
    line = ips_patch.read_patch_line(fake_file)

    assert line.offset == 1
    assert line.data == bytes([2, 2])

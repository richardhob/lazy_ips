
import unittest.mock

import pytest

import lazy_ips.patch.ips as patch_ips

@pytest.fixture(scope="function")
def fake_file():
    image = unittest.mock.MagicMock()
    return image

def test_apply_patch_line(fake_file):
    line = patch_ips.PatchLine(offset=1, data=2)
    patch_ips.apply_patch_line(fake_file, line)

    fake_file.seek.assert_called_once_with(line.offset)
    fake_file.write.assert_called_once_with(line.data)

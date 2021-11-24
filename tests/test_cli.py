
import os
import subprocess

import pytest

PATH_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(PATH_HERE, '..')

@pytest.fixture(scope="function")
def image(tmp_path):
    path = tmp_path / "img.bin"

    with open(path, 'wb') as output:
        for i in range(100):
            output.write(int(0xA5A5A5A5).to_bytes(4, 'big'))
            output.write(int(0x5A5A5A5A).to_bytes(4, 'big'))

    return path

@pytest.fixture(scope="function")
def no_patch(tmp_path):
    path = tmp_path / "no_patch.ips"
    return path

@pytest.fixture(scope="function")
def simple_patch(tmp_path):
    path = tmp_path / "patch.ips"

    with open(path, 'wb') as output:
        output.write(b'PATCH')
        output.write(b'EOF')

    return patch

def call(image, patch):
    subprocess.run(
        "python lazy_ips/cli.py {} {}".format(image, patch),
        cwd=ROOT_PATH,
        shell=True,
        check=True)

def test_cli_no_files(no_patch):
    with pytest.raises(subprocess.CalledProcessError):
        call(no_patch, no_patch)

def test_cli_no_patch(image, no_patch):
    with pytest.raises(subprocess.CalledProcessError):
        call(image, no_patch)

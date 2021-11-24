
import os
import subprocess

import pytest

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

    return path

@pytest.fixture(scope="function")
def patch1(tmp_path):
    path = tmp_path / "patch1.ips"

    with open(path, 'wb') as output:
        output.write(b'PATCH')

        # Location, Size, Data
        output.write(int(0).to_bytes(3, 'big'))
        output.write(int(1).to_bytes(2, 'big'))
        output.write(int(2).to_bytes(1, 'big'))

        output.write(b'EOF')

    return path

@pytest.fixture(scope="function")
def patch2(tmp_path):
    path = tmp_path / "patch2.ips"

    with open(path, 'wb') as output:
        output.write(b'PATCH')

        # Location, Size, Data
        output.write(int(199).to_bytes(3, 'big'))
        output.write(int(4).to_bytes(2, 'big'))
        output.write(int(0xDEADBEEF).to_bytes(4, 'big'))

        output.write(b'EOF')

    return path

@pytest.fixture(scope="function")
def patch3(tmp_path):
    path = tmp_path / "patch3.ips"

    with open(path, 'wb') as output:
        output.write(b'PATCH')

        # Location, 0, RLE Size, RLE Data
        output.write(int(0).to_bytes(3, 'big'))
        output.write(int(0).to_bytes(2, 'big'))
        output.write(int(800).to_bytes(2, 'big'))
        output.write(int(0).to_bytes(1, 'big'))

        output.write(b'EOF')

    return path

def call(image, patch):
    subprocess.run(
        "python -m lazy_ips.cli {} {}".format(image, patch),
        shell=True,
        check=True)

def test_cli_no_files(no_patch):
    with pytest.raises(subprocess.CalledProcessError):
        call(no_patch, no_patch)

def test_cli_no_patch(image, no_patch):
    with pytest.raises(subprocess.CalledProcessError):
        call(image, no_patch)

def test_cli_simple_patch(image, simple_patch):
    call(image, simple_patch)

def test_cli_patch1(image, patch1):
    call(image, patch1)

    with open(image, 'rb') as input_file:
        input_file.seek(0)
        value = input_file.read(1)
        assert value == int(2).to_bytes(1, 'big')

def test_cli_patch2(image, patch2):
    call(image, patch2)

    with open(image, 'rb') as input_file:
        input_file.seek(199)
        value = input_file.read(4)
        assert value == int(0xDEADBEEF).to_bytes(4, 'big')
 
def test_cli_patch3(image, patch3):
    call(image, patch3)

    with open(image, 'rb') as input_file:
        value = input_file.read(800)
        assert value == bytes(800 * [0])

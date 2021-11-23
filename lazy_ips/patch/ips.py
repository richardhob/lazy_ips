
''' IPS Patch File Reading.

IPS File Format (file is in binary format):

|--------|--------------|-------------------------------|
| Name   | Bytes        | Description                   |
|========|==============|===============================|
| header | 5            | "PATCH" (no null character)   |
|--------|--------------|-------------------------------|
| record | 3 + 2 + X    | See Next Table                |
|--------|--------------|-------------------------------|
| eof    | 3            | End of file                   |
|--------|--------------|-------------------------------|

Records Specifically:

|--------|--------------|-------------------------------|
| Name   | Bytes        | Description                   |
|========|==============|===============================|
| offset | 3            | Location in image to change   |
|--------|--------------|-------------------------------|
| size   | 2            | Number of bytes to write      |
|--------|--------------|-------------------------------|
| data   | size         | Data to be written            |
|--------|--------------|-------------------------------|

If the record size is '0', then the record is RLE encoded.

Run-Length Encoding (RLE) Record:

|--------|--------------|-------------------------------|
| Name   | Bytes        | Description                   |
|========|==============|===============================|
| offset | 3            | Location in image to change   |
|--------|--------------|-------------------------------|
| size   | 2            | '0x0000'                      |
|--------|--------------|-------------------------------|
| RLEsize| 2            | Number of RLE bytes to write  |
|--------|--------------|-------------------------------|
| data   | 1            | Data to be written            |
|--------|--------------|-------------------------------|

Data in the patch file is in MSB order.
'''

from collections import namedtuple
from struct import unpack

PatchLine = namedtuple('PatchLine', ['offset', 'data'])

EOF_MARKER = b'EOF'
OFFSET_SIZE = 3  # bytes
DATA_LEN_SIZE = 2  # bytes
RLE_LEN_SIZE = 2  # bytes


def read_patch_line(file):
    ''' Read a line from the patch file, and decode the patch data.

    Args:
        input_file (File): opened IPS patch file

    Returns:
        Named Tuple PatchLine(offset, patch_data)

    Raises:
        IOError if the Offset or Data is formatted incorrectly
    '''
    offset_raw = file.read(OFFSET_SIZE)
    if len(offset_raw) != OFFSET_SIZE:
        raise IOError("not enough offset bytes read")

    if offset_raw == EOF_MARKER:
        return None
  
    offset = unpack('>l', b'\x00' + offset_raw)[0]
    data_len_raw = file.read(DATA_LEN_SIZE)
    if len(data_len_raw) != DATA_LEN_SIZE:
        raise IOError("not enough data len bytes read")

    data_len = unpack('>h', data_len_raw)[0]

    if data_len > 0:
        data = file.read(data_len)
        if len(data) != data_len:
            raise IOError("not enough data bytes read")
        return PatchLine(offset, data)

    # RLE
    rle_len_raw = file.read(RLE_LEN_SIZE)
    if len(rle_len_raw) != RLE_LEN_SIZE:
        raise IOError("not enough rle data len bytes")

    rle_len = unpack('>h', rle_len_raw)[0]
    rle_byte = file.read(1)
    if len(rle_byte) != 1:
        raise IOError("not enough rle data bytes")

    data = rle_byte * rle_len
    return PatchLine(offset, data)


def read_patch(file):
    ''' Read the input patch file, and generate patch line data (offset, data).

    Args:
        input_file (Path): Path to the input patch file

    Generates:
        Data from patch file (offset, data)

    Raises:
        IOError if Patch file is misformatted
    '''
    # Constant
    patch_marker = b'PATCH'

    # Check marker.
    data = file.read(len(patch_marker))
    if data != patch_marker:
        raise IOError("unknown format")

    eof = False
    while not eof:
        data = read_patch_line(file)
        if data:
            yield data
        else:
            eof = True


def apply_patch_line(image, patch_line):
    ''' Apply input line from patch file to the input image.

    Args:
        image (File): Image file to be patched
        patch_line (PatchLine): Offset and Data to patch in the image
    '''
    try:
        image.seek(patch_line.offset)
    except Exception:
        # Go to the 0th line from the end of the file (EOF)
        image.seek(0, 2)
    image.write(patch_line.data)

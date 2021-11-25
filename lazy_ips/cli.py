#!/usr/bin/env python3

import shutil
import sys
import argparse

from lazy_ips.patch import ips


def main():
    parser = argparse.ArgumentParser(
            description="Apply IPS patch to ROM image")
    parser.add_argument("image_file")
    parser.add_argument("patch_file")
    parser.add_argument("-o", help="Separate output file")

    args = parser.parse_args()

    image_file = args.image_file
    if args.o:
        shutil.copyfile(args.image_file, args.o)
        image_file = args.o

    try:
        image = open(image_file, 'rb+')
    except Exception as err:
        print("Error opening {}: {}".format(image_file, err))
        sys.exit(1)

    try:
        patch = open(args.patch_file, 'rb')
    except Exception as err:
        image.close()
        print("Error opening {}: {}".format(args.patch_file, err))
        sys.exit(2)

    try:
        for patch_line in ips.read_patch(patch):
            ips.apply_patch_line(image, patch_line)
    except Exception as err:
        print("Error patching {}: {}".format(args.image_file, err))
    finally:
        patch.close()
        image.close()


if __name__ == "__main__":
    main()

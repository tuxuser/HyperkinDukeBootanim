#!/usr/bin/env python3

"""
Handle YC25Q32B flash image operations for Hyperkin Duke Xbox One controller
* Extract filesystem image
* Inject filesystem image
Creates a ready-to-flash image

Usage for extraction:
flashdump_tool.py extract YC25Q32B_dump.bin fat16_fs.img
Usage for injection:
flashdump_tool.py inject --fsimg fat16_fs_new.img YC25Q32B_dump.bin ready_to_flash.bin

Author: tuxuser @ 01/2020
"""

import sys
import os
import argparse

FLASH_IMAGE_SIZE = 0x400000

FAT16_IMAGE_OFFS = 0x10D000
FAT16_IMAGE_SIZE = 0x2F3000

def is_valid_file(x, expected_size):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    elif os.path.getsize(x) != expected_size:
        raise argparse.ArgumentTypeError(
            "{0} is not valid, expected filesize: {1} bytes".format(x, expected_size)) 
    return x

def extract_filesystem_img(flash_dump_path, output_fsimg_path):
    with open(flash_dump_path, 'rb') as fi:
        # Seek to FAT16 image offset
        fi.seek(FAT16_IMAGE_OFFS, 0)
        fs_data = fi.read(FAT16_IMAGE_SIZE)
        assert fi.read() == b''

    with open(output_fsimg_path, 'wb') as fo:
        fo.write(fs_data)

def inject_filesystem_img(flash_dump_path, fsimg_path, output_flashimage_path):
    with open(flash_dump_path, 'rb') as fi:
        with open(fsimg_path, 'rb') as fs:
            with open(output_flashimage_path, 'wb') as out:
                # Read original bootloader portion
                bootloader_data = fi.read(FAT16_IMAGE_OFFS)
                # Read supplied filesystem data
                fs_data = fs.read(FAT16_IMAGE_SIZE)

                # Assemble final file
                out.write(bootloader_data)
                out.write(fs_data)

                assert out.tell() == FLASH_IMAGE_SIZE


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Handle Hyperkin Duke flash image operation')
    parser.add_argument('action', choices=['extract', 'inject'],
                        help='Action to take')
    parser.add_argument('flash_dump',
                        type=lambda x: is_valid_file(x, FLASH_IMAGE_SIZE),
                        help='Flash dump to operate on')
    parser.add_argument('output_file',
                        help='Output file location'
                             ' (e.g. [extract] => filesystem image,'
                             ' [inject] => full flash image)')
    parser.add_argument('--fsimg',
                        type=lambda x: is_valid_file(x, FAT16_IMAGE_SIZE),
                        help='FAT16 filesystem image to inject (used for action [inject])')

    args = parser.parse_args()

    if args.action == 'inject' and not args.fsimg:
        print("Error: Action [inject] requires --fsimg parameter!")
        sys.exit(2)
    elif args.action == 'inject':
        print('[+] Injecting filesystem image {0} into {1} => output file: {2}...'.format(
            args.fsimg, args.flash_dump, args.output_file))
        inject_filesystem_img(args.flash_dump, args.fsimg, args.output_file)
    elif args.action == 'extract':
        print('[+] Extracting filesystem image to {0}...'.format(args.output_file))
        extract_filesystem_img(args.flash_dump, args.output_file)
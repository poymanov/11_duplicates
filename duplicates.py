import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to directory for scan')
    return parser.parse_args()


def scan_directory(path):
    if not os.path.isdir(path):
        return None

    files_info = {}

    for dir_name, subdir_list, file_list in os.walk(path):
        for filename in file_list:
            filepath = os.path.join(dir_name, filename)
            filesize = os.path.getsize(filepath)
            files_info.setdefault((filename, filesize), []).append(filepath)

    return files_info


def get_duplicates_info(files_stats):
    duplicates_info = []
    for paths in files_stats.values():
        if len(paths) > 1:
            duplicates_info.append(paths)

    return duplicates_info


def output_duplicates_to_console(duplicates_info):
    if not duplicates_info:
        print('There are not files duplicates in directory')
    else:
        print('Duplicates founded:', '\n')
        for paths in duplicates_info:
            print('\n' . join(paths), '\n')


if __name__ == '__main__':
    args = parse_args()

    path = args.path
    files_info = scan_directory(path)

    if files_info is None:
        sys.exit("Directory doesn't exist")

    if not files_info:
        sys.exit('Directory is empty')

    duplicates_info = get_duplicates_info(files_info)

    output_duplicates_to_console(duplicates_info)

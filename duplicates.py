import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to directory for scan')
    return parser.parse_args()


def get_file_id(filename, filesize):
    return '{}_{}'.format(filename, filesize)


def scan_directory(path):
    if not os.path.isdir(path):
        return None

    files_info = []

    for dir_name, subdir_list, file_list in os.walk(path):
        for filename in file_list:
            filepath = os.path.join(dir_name, filename)
            filesize = os.path.getsize(filepath)

            file_id = get_file_id(filename, filesize)
            files_info.append((file_id, filepath))

    files_stats = {}

    for file_id, filepath in files_info:
        files_stats.setdefault(file_id, []).append(filepath)

    return files_stats


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
    files_stats = scan_directory(path)

    if files_stats is None:
        sys.exit('Directory doesn\'t exist')

    if not files_stats:
        sys.exit('Directory is empty')

    duplicates_info = get_duplicates_info(files_stats)

    output_duplicates_to_console(duplicates_info)

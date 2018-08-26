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

    files_list = []

    for dir_name, subdir_list, file_list in os.walk(path):
        for file_name in file_list:
            files_list.append(dir_name + '/' + file_name)

    return files_list


def get_files_info(files_list):
    files_info = {}
    for file in files_list:
        file_name = os.path.basename(file)
        file_size = os.path.getsize(file)

        seach_key = '{}_{}'.format(file_name, file_size)

        if seach_key not in files_info:
            files_info[seach_key] = [file]
        else:
            files_info[seach_key].append(file)

    return files_info


def get_duplicates(files_info):
    duplicates_info = []
    for files_paths in files_info.values():
        if len(files_paths) == 1:
            continue
        duplicates_info.append(files_paths)
    return duplicates_info


if __name__ == '__main__':
    args = parse_args()

    path = args.path
    files_list = scan_directory(path)

    if files_list is None:
        sys.exit("Directory doesn't exist")

    if not files_list:
        sys.exit("Directory is empty")

    files_info = get_files_info(files_list)
    duplicates_info = get_duplicates(files_info)

    if not duplicates_info:
        sys.exit("There are not files duplicates in directory")

    print('Duplicates founded:', '\n')
    for duplicate_paths in duplicates_info:
        for duplicate_file_path in duplicate_paths:
            print(duplicate_file_path)
        print('\n')

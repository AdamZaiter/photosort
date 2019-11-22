import sys
import os
import shutil
from distutils.dir_util import copy_tree
import renameAndGPS as RG


def copy_files(src_dir, dest_dir):
    if os.path.isdir(src_dir):

        copy_tree(src_dir, dest_dir)
        print('Files successfuly copied to destination directory.')

    else:
        print('Invalid source directory')
        sys.exit()

    if not os.path.isdir(dest_dir):
        print('Destination folder couldn\'t be accessed or created')
        sys.exit()


flags_dict = {'-x': False, '-m': False}
# print(flags_dict)
sys.argv
if len(sys.argv) == 1 or (len(sys.argv) < 3 and sys.argv[1] != '--help'):
    print('Usage: movefiles.py source_folder destination_folder')
    print('For additional commands info type --help')
    sys.exit()

if sys.argv[1] == '--help':
    print('Flags:\n-x  removes source directory after copying files')
    sys.exit()
elif len(sys.argv) < 3:
    print('Usage: movefiles.py source_folder destination_folder')
    print('For additional flags info type --help')


# checking for flags in args
for i in range(3, len(sys.argv)):
    if sys.argv[i] in flags_dict:
        flags_dict[sys.argv[i]] = True
    else:
        print('You used an invalid flag.\nType --help for list of commands.')
        sys.exit()
# copy subdirectory example
# print(flags_dict)
src_dir = (sys.argv[1])
dest_dir = (sys.argv[2])

copy_files(src_dir, dest_dir)

if flags_dict['-x']:
    shutil.rmtree(src_dir, ignore_errors=True)
    print('Source directory successfuly removed.')

lists = RG.rename_files(dest_dir, flags_dict)
list_of_gps = lists[0]
list_of_filenames = lists[1]
list_of_converted_gps = []
if list_of_gps and flags_dict['-m']:
    for coordinates in list_of_gps:
        list_of_converted_gps.append(
            RG.convert_gps_to_degrees(coordinates[0], coordinates[1]))
    RG.get_map(list_of_converted_gps, dest_dir, list_of_filenames)

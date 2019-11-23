import sys
import os
import shutil
from distutils.dir_util import copy_tree
import rename as R
import GPS


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

sys.argv
if len(sys.argv) == 1 or (len(sys.argv) < 3 and sys.argv[1] != '--help'):
    print('Usage: movefiles.py source_folder destination_folder')
    print('For additional commands info type --help')
    sys.exit()

if sys.argv[1] == '--help':
    print('Flags:\n-x  removes source directory after copying files')
    print('-m  creates a google map with GPS coordinates of photos')
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


src_dir = (sys.argv[1])
dest_dir = (sys.argv[2])

copy_files(src_dir, dest_dir)

if flags_dict['-x']:
    shutil.rmtree(src_dir, ignore_errors=True)
    print('Source directory successfuly removed.')

R.rename_files(dest_dir, flags_dict)

if flags_dict['-m']:
    directory = dest_dir + '\\photos'
    list_of_gps = GPS.get_GPS(directory)
    if list_of_gps:
        list_of_degrees = GPS.convert_gps_to_degrees(list_of_gps)
        GPS.get_map(list_of_degrees, dest_dir)
    else:
        print('GPS coordinates couldn\'t be retrieved.')

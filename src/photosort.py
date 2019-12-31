import sys
import os
import shutil
import rename
import GPS
import GUI
import argparse


def copy_files(src_dir: str, dest_dir: str, verbose: bool) -> None:
    '''
    Copies files into existing directory or creates a new one.
    '''
    if os.path.isdir(src_dir):
        if not os.path.exists(dest_dir):
            try:
                os.mkdir(dest_dir)
            except:
                print("Destination directory couldn't be accessed or created.")
                sys.exit()

        for (dirpath, dirnames, filenames) in os.walk(src_dir):
            for filename in filenames:
                if verbose:
                    print(f'{filename} is being copied.')

                try:
                    shutil.copy2(src_dir + '/' + filename, dest_dir)
                except FileNotFoundError:
                    print('File not found.')
                    sys.exit()

    else:
        print('Invalid source directory.')
        print('Usage: movefiles.py source_folder destination_folder')
        sys.exit()

    print('Files successfuly copied.')


def flag_handling() -> None:
    '''
    Goes through flags and executes their functions.
    '''
    if args.remove:
        shutil.rmtree(src_dir, ignore_errors=True)
        print('Source directory successfuly removed.')

    if args.map:
        directory = dest_dir + '/' + 'photos'
        list_of_gps = GPS.get_GPS(directory)
        if list_of_gps:
            list_of_degrees = GPS.convert_gps_to_degrees(list_of_gps)
            GPS.get_map(list_of_degrees, dest_dir)
        else:
            print('GPS coordinates couldn\'t be retrieved.')


if len(sys.argv) == 1:
    GUI.gui_photosort()
    sys.exit()
parser = argparse.ArgumentParser(
    description='Copy photos from one folder to another and rename them')
parser.add_argument('src_dir')
parser.add_argument('dest_dir')
parser.add_argument('-x', '--remove', action='store_true',
                    help='Removes source directory after copying files')
parser.add_argument('-m', '--map', action='store_true',
                    help='Creates a google map with GPS coordinates of photos')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Adds verbosity')
args = parser.parse_args()
gui = False
print(type(args))
src_dir = args.src_dir
dest_dir = args.dest_dir


copy_files(src_dir, dest_dir, args.verbose)

rename.rename_files(dest_dir, gui)
print('Files renamed.')
flag_handling()

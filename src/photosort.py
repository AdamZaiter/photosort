import sys
import os
import shutil
import rename
import GPS
import GUI


def copy_files(src_dir: str, dest_dir: str) -> None:
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
                print(f'{filename} is being copied.')

                shutil.copy2(src_dir + '/' + filename, dest_dir)

    else:
        print('Invalid source directory.')
        print('Usage: movefiles.py source_folder destination_folder')
        sys.exit()

    print('Files successfuly copied.')


def flag_handling(flags_dict: dict) -> None:
    '''
    Goes through flags and executes their functions.
    '''
    if flags_dict['-x']:
        shutil.rmtree(src_dir, ignore_errors=True)
        print('Source directory successfuly removed.')

    if flags_dict['-m']:
        directory = dest_dir + '/' + 'photos'
        list_of_gps = GPS.get_GPS(directory)
        if list_of_gps:
            list_of_degrees = GPS.convert_gps_to_degrees(list_of_gps)
            GPS.get_map(list_of_degrees, dest_dir)
        else:
            print('GPS coordinates couldn\'t be retrieved.')


flags_dict = {'-x': False, '-m': False}
if len(sys.argv) == 1:
    GUI.gui_photosort()
    sys.exit()
if len(sys.argv) < 3 and sys.argv[1] != '--help':
    print('Usage: movefiles.py source_folder destination_folder')
    print('For additional commands info type --help')
    sys.exit()

if sys.argv[1] == '--help':
    print('Usage: movefiles.py source_folder destination_folder')
    print('Flags:\n-x  removes source directory after copying files')
    print('-m  creates a google map with GPS coordinates of photos')
    sys.exit()
elif len(sys.argv) < 3:
    print('Usage: movefiles.py source_folder destination_folder')
    print('For additional flags info type --help')

gui = False
# checking for flags in args
for i in range(3, len(sys.argv)):
    if sys.argv[i] in flags_dict:
        flags_dict[sys.argv[i]] = True
    else:
        print('You used an invalid flag.')
        print('Usage: movefiles.py source_folder destination_folder')
        print('For additional flags info type photosort.py --help')
        sys.exit()

src_dir = (sys.argv[1])
dest_dir = (sys.argv[2])
if src_dir == dest_dir:
    print('Directories cannot be the same!')
    sys.exit()

copy_files(src_dir, dest_dir)

rename.rename_files(dest_dir, gui)
print('Files renamed.')
flag_handling(flags_dict)

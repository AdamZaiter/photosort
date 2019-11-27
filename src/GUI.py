import PySimpleGUI as sg
import sys
import os
import shutil
import rename
import GPS


def copy_files(src_dir, dest_dir):
    if os.path.isdir(src_dir):
        progress, counter_of_files = 0, 0
        if not os.path.exists(dest_dir):
            try:
                os.mkdir(dest_dir)
            except:
                sg.popup("Destination directory couldn't be accessed or created.")
                sys.exit()

        for (dirpath, dirnames, filenames) in os.walk(src_dir):
            # counting number of files for the progress meter
            for filename in filenames:
                counter_of_files += 1
        for (dirpath, dirnames, filenames) in os.walk(src_dir):
            for filename in filenames:
                print(f'{filename} is being copied.')
                shutil.copy2(src_dir + '/' + filename, dest_dir)
                progress += 1
                sg.OneLineProgressMeter(
                    'photosort', progress, counter_of_files, 'key', 'Copying files')

    else:
        sg.popup('Invalid source directory')
        sys.exit()

    return counter_of_files


def flag_handling(flags_dict, dest_dir):
    if flags_dict['-x']:
        shutil.rmtree(src_dir, ignore_errors=True)
        sg.popup('Source directory successfuly removed.')

    if flags_dict['-m']:
        directory = dest_dir + '/' + 'photos'
        list_of_gps = GPS.get_GPS(directory)
        if list_of_gps:
            list_of_degrees = GPS.convert_gps_to_degrees(list_of_gps)
            GPS.get_map(list_of_degrees, dest_dir)
            sg.popup('Google map drawn.')

        else:
            sg.popup('GPS coordinates couldn\'t be retrieved.')


def gui_photosort():
    gui = True
    flags_dict = {'-x': False, '-m': False}
    sg.change_look_and_feel('Dark')
    layout = [[sg.Text('Enter 2 folders')],
              [sg.Text('Folder to copy', size=(15, 1)),
               sg.Input(), sg.FolderBrowse()],
              [sg.Text('Folder where to copy', size=(15, 1)),
               sg.Input(), sg.FolderBrowse()],
              [sg.Checkbox('Remove source directory', size=(20, 1), key='check1'),
               sg.Checkbox('Add a google map based on GPS data', key='check2')],
              [sg.Submit(), sg.Cancel()]]
    window = sg.Window('photosort', layout)
    event, values = window.read()
    window.close()
    src_dir = values[0]
    dest_dir = values[1]
    flags_dict['-x'] = values['check1']
    flags_dict['-m'] = values['check2']
    if event in (None, 'Cancel'):
        sys.exit()
    if src_dir == dest_dir:
        sg.popup('Directories cannot be the same!')
        sys.exit()

    num_of_files = copy_files(src_dir, dest_dir)

    rename.rename_files(dest_dir, flags_dict, gui, num_of_files)
    sg.popup('Files successfuly copied to destination directory and renamed.')

    flag_handling(flags_dict, dest_dir)

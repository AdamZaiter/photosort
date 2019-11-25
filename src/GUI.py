import PySimpleGUI as sg
import sys
import os
import shutil
from distutils.dir_util import copy_tree
import rename as R
import GPS

SLASH = '\\'

if os.name == 'posix':
    SLASH = '/'


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


def flag_handling(flags_dict, dest_dir):
    if flags_dict['-x']:
        shutil.rmtree(src_dir, ignore_errors=True)
        sg.popup('Source directory successfuly removed.')

    if flags_dict['-m']:
        directory = dest_dir + SLASH + 'photos'
        list_of_gps = GPS.get_GPS(directory)
        if list_of_gps:
            list_of_degrees = GPS.convert_gps_to_degrees(list_of_gps)
            GPS.get_map(list_of_degrees, dest_dir)
        else:
            sg.popup('GPS coordinates couldn\'t be retrieved.')
        sg.popup('Google map drawn.')


def gui_photosort():
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

    copy_files(src_dir, dest_dir)

    R.rename_files(dest_dir, flags_dict)
    sg.popup('Files successfuly copied to destination directory and renamed.')
    flag_handling(flags_dict, dest_dir)


if __name__ == '__main__':

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

    copy_files(src_dir, dest_dir)

    R.rename_files(dest_dir, flags_dict)
    sg.popup('Files successfuly copied to destination directory and renamed.')
    flag_handling(flags_dict)

from PIL import Image
import os
import sys
import PySimpleGUI as sg


def get_date_taken(path: str) -> None:
    '''
    Returns a date when image was taken.
    '''
    DATETag = 36867
    try:
        img = Image.open(path)
        info = img.getexif()
        try:
            return info[DATETag]
        except KeyError:
            pass
    except IOError:
        pass


def rename_files(dest_dir: str, gui: bool, num_of_files=0) -> None:
    '''
    Organizes files into photos/year(unknown), then renames files
    with a format YYYY-MM-DD-XXX
    '''
    os.chdir(dest_dir)
    used_file_names = []
    progress = 0
    try:
        os.listdir(dest_dir)
    except FileNotFoundError:
        print('Destination directory was not found. Be sure to use absolute paths.')
        sys.exit()
    for old_file_name in os.listdir(dest_dir):
        path_to_image = dest_dir + '/' + old_file_name
        date_taken = get_date_taken(path_to_image)
        if not date_taken:
            number_string = '001'
            new_file_name = 'photos/unknown/' + number_string + '.jpg'
            while new_file_name in used_file_names:
                if int(number_string) < 10:
                    number_string = int(number_string) + 1
                    number_string = '00' + str(number_string)
                    new_file_name = 'photos/unknown/' + number_string + '.jpg'
                elif int(number_string) < 100:
                    number_string = int(number_string) + 1
                    number_string = '0' + str(number_string)
                    new_file_name = 'photos/unknown/' + number_string + '.jpg'
                else:
                    number_string = int(number_string) + 1
                    number_string = str(number_string)
                    new_file_name = 'photos/unknown/' + number_string + '.jpg'
            dest_dir_format = dest_dir + '/' + old_file_name
            used_file_names.append(new_file_name)
            try:
                os.renames(dest_dir_format, new_file_name)
            except:
                print('Permission denied')
                sys.exit()

        else:
            year = date_taken[0:4]
            formatted_date = date_taken.replace(':', '-')
            list_date_time = formatted_date.split()
            date = list_date_time[0]
            number_string = '001'
            new_file_name = 'photos/' + year + '/' + \
                date + '-' + number_string + '.jpg'
            # rename a file if it matches a name that was already used
            while new_file_name in used_file_names:
                if int(number_string) < 10:
                    number_string = int(number_string) + 1
                    number_string = '00' + str(number_string)
                    new_file_name = 'photos/' + year + '/' + \
                        date + '-' + number_string + '.jpg'
                elif int(number_string) < 100:
                    number_string = int(number_string) + 1
                    number_string = '0' + str(number_string)
                    new_file_name = 'photos/' + year + '/' + \
                        date + '-' + number_string + '.jpg'
                else:
                    number_string = int(number_string) + 1
                    number_string = str(number_string)
                    new_file_name = 'photos/' + year + '/' + \
                        date + '-' + number_string + '.jpg'

            used_file_names.append(new_file_name)
            os.renames(old_file_name, new_file_name)
        progress += 1
        if gui:
            sg.OneLineProgressMeter(
                'photosort', progress, num_of_files, 'key', 'Renaming files')

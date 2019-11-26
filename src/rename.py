from PIL import Image
import os
import sys
import PySimpleGUI as sg

DATETag = 36867
SLASH = '\\'
if os.name == 'posix':
    SLASH = '/'


def get_date_taken(path):
    try:
        img = Image.open(path)
        info = img.getexif()
        try:
            return info[DATETag]
        except KeyError:
            pass
    except IOError:
        pass


def rename_files(dest_dir, flags_dict, gui, num_of_files=0):
    os.chdir(dest_dir)
    used_file_names = []
    i = 0
    for filename in os.listdir(dest_dir):
        try:
            with open(dest_dir + SLASH + filename, 'rb') as f:
                date_taken = get_date_taken(dest_dir + SLASH + filename)
                if not date_taken:
                    number_string = '001'
                    file_name = 'photos/unknown/' + number_string + '.jpg'
                    while file_name in used_file_names:
                        if int(number_string) < 10:
                            number_string = int(number_string) + 1
                            number_string = '00' + str(number_string)
                            file_name = 'photos/unknown/' + number_string + '.jpg'
                        elif int(number_string) < 100:
                            number_string = int(number_string) + 1
                            number_string = '0' + str(number_string)
                            file_name = 'photos/unknown/' + number_string + '.jpg'
                        else:
                            number_string = int(number_string) + 1
                            number_string = str(number_string)
                            file_name = 'photos/unknown/' + number_string + '.jpg'
                    dest_dir_format = dest_dir + SLASH + filename
                    used_file_names.append(file_name)
                    f.close()
                    os.renames(dest_dir_format, file_name)

                else:
                    year = []
                    date_taken = str(date_taken)
                    for num in date_taken:
                        if num == ':':
                            break
                        else:
                            year.append(num)
                    formatted_date = str(date_taken.replace(':', '-'))
                    formatted_date = formatted_date.split()
                    formatted_date = formatted_date[0]
                    year = "".join(year)

                    number_string = '001'
                    file_name = 'photos/' + year + SLASH + \
                        formatted_date + '-' + number_string + '.jpg'

                    while file_name in used_file_names:
                        if int(number_string) < 10:
                            number_string = int(number_string) + 1
                            number_string = '00' + str(number_string)
                            file_name = 'photos/' + year + SLASH + \
                                formatted_date + '-' + number_string + '.jpg'
                        elif int(number_string) < 100:
                            number_string = int(number_string) + 1
                            number_string = '0' + str(number_string)
                            file_name = 'photos/' + year + SLASH + \
                                formatted_date + '-' + number_string + '.jpg'
                        else:
                            number_string = int(number_string) + 1
                            number_string = str(number_string)
                            file_name = 'photos/' + year + SLASH + \
                                formatted_date + '-' + number_string + '.jpg'

                    used_file_names.append(file_name)

                    dest_dir_format = dest_dir + SLASH + filename
                    f.close()
                    os.renames(dest_dir_format, file_name)
                i += 1
                if gui:
                    sg.OneLineProgressMeter(
                        'photosort', i, num_of_files, 'key', 'Renaming files')
        except:
            if gui:
                sg.popup('Error. Permission denied. Try different directory.')
            else:
                print('Error. Permission denied. Try different directory.')
            sys.exit()

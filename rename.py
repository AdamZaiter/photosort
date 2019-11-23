from PIL import Image
import os
DATETag = 36867


def get_date_taken(path):
    try:
        return Image.open(path)._getexif()[DATETag]
    except IOError:
        pass


#dest_dir = 'C:\\Users\\zaite\\new'


def rename_files(dest_dir, flags_dict):
    os.chdir(dest_dir)
    used_file_names = []
    for filename in os.listdir(dest_dir):
        with open(dest_dir + '\\' + filename, 'rb') as f:
            date_taken = get_date_taken(dest_dir + '\\' + filename)
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
                dest_dir_format = dest_dir + '\\' + filename
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
                file_name = 'photos/' + year + '/' + \
                    formatted_date + '-' + number_string + '.jpg'

                while file_name in used_file_names:
                    if int(number_string) < 10:
                        number_string = int(number_string) + 1
                        number_string = '00' + str(number_string)
                        file_name = 'photos/' + year + '/' + \
                            formatted_date + '-' + number_string + '.jpg'
                    elif int(number_string) < 100:
                        number_string = int(number_string) + 1
                        number_string = '0' + str(number_string)
                        file_name = 'photos/' + year + '/' + \
                            formatted_date + '-' + number_string + '.jpg'
                    else:
                        number_string = int(number_string) + 1
                        number_string = str(number_string)
                        file_name = 'photos/' + year + '/' + \
                            formatted_date + '-' + number_string + '.jpg'

                used_file_names.append(file_name)

                dest_dir_format = dest_dir + '\\' + filename
                f.close()
                os.renames(dest_dir_format, file_name)

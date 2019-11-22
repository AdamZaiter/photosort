from PIL import Image, ExifTags
import gmplot
import os
DATETag = 36867
list_of_filenames = []


def convert_gps_to_degrees(latitude, longitude):
    lat_degree = list(latitude[0])
    lat_degree = lat_degree[0] / lat_degree[1]
    lat_minute = list(latitude[1])
    lat_minute = lat_minute[0] / lat_minute[1]
    lat_minute = lat_minute / 60
    lat_second = list(latitude[2])
    lat_second = lat_second[0] / lat_second[1]
    lat_second = lat_second / 3600

    long_degree = list(longitude[0])
    long_degree = long_degree[0] / long_degree[1]
    long_minute = list(longitude[1])
    long_minute = long_minute[0] / long_minute[1]
    long_minute = long_minute / 60
    long_second = list(longitude[2])
    long_second = long_second[0] / long_second[1]
    long_second = long_second / 3600
    return lat_degree + lat_minute + lat_second, long_degree + long_minute + long_second


def get_GPS(filename):
    try:
        img = Image.open(filename)
        exif = {ExifTags.TAGS[k]: v for k,
                v in img._getexif().items() if k in ExifTags.TAGS}
        gpsinfo = {}
        for key in exif['GPSInfo'].keys():
            decode = ExifTags.GPSTAGS.get(key, key)
            gpsinfo[decode] = exif['GPSInfo'][key]
        latitude = gpsinfo['GPSLatitude']
        longitude = gpsinfo['GPSLongitude']
        return latitude, longitude
    except:
        pass


def get_map(list_of_converted_gps, dest_dir, list_of_filenames):

    gmap = gmplot.GoogleMapPlotter(
        list_of_converted_gps[0][0], list_of_converted_gps[0][1], 10)
    for i, coordinates in enumerate(list_of_converted_gps):
        gmap.marker(coordinates[0], coordinates[1],
                    'cornflowerblue', title=list_of_filenames[i])
    # Pass the absolute path
    gmap.draw(dest_dir + '\\gpsmap.html')
    print('Google map drawn.')


def get_date_taken(path):
    try:
        return Image.open(path)._getexif()[DATETag]
    except IOError:
        pass


#dest_dir = 'C:\\Users\\zaite\\new'


def rename_files(dest_dir, flags_dict):
    list_of_coordinates = []
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

                if flags_dict['-m']:
                    list_of_coordinates.append(get_GPS(dest_dir + '\\' + file_name))
                if None in list_of_coordinates:
                    list_of_coordinates.remove(None)
                else:
                    list_of_filenames.append(file_name)
    return list_of_coordinates, list_of_filenames
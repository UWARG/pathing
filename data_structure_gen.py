# I got tired of copy pasting everytime
import utm

diction = {}

file = open("Waypoints.csv")


def list(latlon, name):
    temp_list = []
    for line in file:
        coord, name = line.split(',')
        lon, lat = coord[7:-1].split()

        if (latlon == True) and (name == True):
            temp_list.append((name.strip(), float(lat), float(lon)))
        elif (latlon == False) and (name == True):
            temp_list.append(
                (name.strip(), utm.from_latlon(float(lat), float(lon))[0], utm.from_latlon(float(lat), float(lon))[1]))
        elif (latlon == True) and (name == False):
            temp_list.append((float(lat), float(lon)))
        else:
            temp_list.append((utm.from_latlon(float(lat), float(lon))[0], utm.from_latlon(float(lat), float(lon))[1]))
    return temp_list


def dictionary(latlon, name):
    temp_dict = {}
    for line in file:
        coord, name = line.split(',')
        lon, lat = coord[7:-1].split()
        if latlon == True:
            temp_dict[name.strip()] = (float(lat), float(lon))
        else:
            temp_dict[name.strip()] = (
            utm.from_latlon(float(lat), float(lon))[0], utm.from_latlon(float(lat), float(lon))[1])
    return temp_dict

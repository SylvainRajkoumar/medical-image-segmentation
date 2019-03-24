import math
import json

radius_average = 0
def get_xyz_points(lines):
    data_xyz = []
    for line in lines:
        data_xyz.append([float(i) for i in line.split(' ')[:3]])
    return data_xyz

def get_radius(lines):
    data_radius = []
    for line in lines:
        data_radius.append(float(line.split(' ')[3:4][0]))
    return data_radius

def compute_average_radius(radius_list):
    compute_average = 0
    for i in range(10):
        compute_average += radius_list[i]
    compute_average /= 10
    return compute_average

def compute_3d_distance(a, b):
    distance = math.sqrt( math.pow(b[0] - a[0], 2)
                        + math.pow(b[1] - a[1], 2)
                        + math.pow(b[2] - a[2], 2) 
                        )
    return distance

def compute_cumulated_distance(point_list):
    cumulated_distance = 0
    for i in range(len(point_list)-1):
        cumulated_distance += compute_3d_distance(point_list[i], point_list[i+1])
    return cumulated_distance

def compute_fall_points(point_list):
    nb_fall_points = 0
    for i in range(len(point_list) - 2):
        if point_list[i][1] < point_list[i+1][1]:
            if point_list[i+1][1] > point_list[i+2][1]: 
                print(point_list[i+2])
                nb_fall_points += 1
    return nb_fall_points

def compute_arter_type(a, b, radius ):
    distance = abs(b-a)
    arter_type=""
    print(f"distance {distance} mm")

    if distance > 2*radius:
        arter_type = "arter type 3"
    elif distance < 2*radius and distance > radius:
        arter_type = "arter type 2"
    elif distance < radius:
        arter_type = "arter type 1"
    return arter_type

if __name__ == "__main__":
    data = {}
    
    with open('centerlinespoints.dat', "r") as fp:  
        lines = fp.readlines()  

        header = lines[0]
        lines.pop(0)

        coords = get_xyz_points(lines)
        radius = get_radius(lines)

        radius_average = compute_average_radius(radius)

        centerline_length = compute_cumulated_distance(coords)
        short_lenght = compute_3d_distance(coords[0], coords[-1])

        tortuosity = centerline_length/short_lenght

        fall_point = compute_fall_points(coords)

        print(f"centerlines length {centerline_length} mm")
        print(f"short length {short_lenght} mm")
        print(f"tortuosity {tortuosity}")
        print(f"average radius {radius_average} mm")
        print(f"number of fallpoints {fall_point}")

        data['centerlines length'] = centerline_length
        data['short length'] = short_lenght
        data['tortuosity'] = tortuosity
        data['average radius'] = radius_average
        data['number of fallpoints'] = fall_point

    with open('typearterpoint.dat', "r") as fp: 
        lines = fp.readlines()  
        header = lines[0]
        lines.pop(0)

        coords = get_xyz_points(lines)
        coord_start = coords[0][1]
        coord_end = coords[-1][1]

        arter_type = compute_arter_type(coord_start, coord_end, radius_average)
        data['arter type'] = arter_type
        print(arter_type)

    with open('data.json', 'w') as outfile:  
        json.dump(data, outfile)
        


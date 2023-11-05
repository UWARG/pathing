
import csv





def run() -> int:
    waypoints = []
    with open('waypoints2024.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                print(f'Name: {row[0]}, latitude: {row[1]}, longitude: {row[2]}')
                waypoint = [float(row[1]), float(row[2])]
                waypoints.append(waypoint)
            line_count += 1
        print(waypoints)

    return 0


if __name__ == "__main__":
    result_run = run()
    if result_run < 0:
        print("ERROR")
    print("Done")

import time
import random
import sys
import os

# http://patorjk.com/software/taag/
print(" _ __ ___     __ _   _ __   ___     _ __    ___   __   __   ___   _ __ ")
print("| '_ ` _ \   / _` | | '__| / __|   | '__|  / _ \  \ \ / /  / _ \ | '__|")
print("| | | | | | | (_| | | |    \__ \   | |    | (_) |  \ V /  |  __/ | |   ")
print("|_| |_| |_|  \__,_| |_|    |___/   |_|     \___/    \_/    \___| |_|   ")
print("")

MissionSafe = True


def send_commands_to_mars(commands):
    print("> Sending commands to mars.")
    timing_list = list(random.random() for i in range(16))
    total_time = sum(timing_list)
    total_send_time = 2 # seconds
    for i in range(len(timing_list)):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(total_send_time*timing_list[i]/total_time)
    print("Complete!")


def orientation_to_direction(orientation):
    if orientation == [0, 1]:
        return 'N'
    if orientation == [0, -1]:
        return 'S'
    if orientation == [1, 0]:
        return 'E'
    if orientation == [-1, 0]:
        return 'W'


def direction_to_orientation(direction):
    if direction == 'N':
        return [0, 1]
    if direction == 'S':
        return [0, -1]
    if direction == 'E':
        return [1, 0]
    if direction == 'W':
        return [-1, 0]


def reorient(current_direction, rotation):
    if rotation == 'L':
        return [-1 * current_direction[1], 1 * current_direction[0]]
    if rotation == 'R':
        return [1 * current_direction[1], -1 * current_direction[0]]
    print("Abort: Re-orientation not understood!")
    return 1/0

# Test Rotation Module
# Sending a rover to mars is surely 'mission critical', so test module with each run.
try:
    assert orientation_to_direction(reorient(direction_to_orientation('N'), 'L')) == 'W'
    assert orientation_to_direction(reorient(direction_to_orientation('S'), 'L')) == 'E'
    assert orientation_to_direction(reorient(direction_to_orientation('E'), 'L')) == 'N'
    assert orientation_to_direction(reorient(direction_to_orientation('W'), 'L')) == 'S'
    assert orientation_to_direction(reorient(direction_to_orientation('N'), 'R')) == 'E'
    assert orientation_to_direction(reorient(direction_to_orientation('S'), 'R')) == 'W'
    assert orientation_to_direction(reorient(direction_to_orientation('E'), 'R')) == 'S'
    assert orientation_to_direction(reorient(direction_to_orientation('W'), 'R')) == 'N'
except:
    MissionSafe = False
    print("Failure in rotation module.")


def move(current, orientation):
    return [current[0] + orientation[0], current[1] + orientation[1]]

# Test Move Module (Mission Critical)
try:
    assert move([1, 2], [0, 1]) == [1, 3]
except:
    MissionSafe = False
    print("Failure of move module.")


def map_area(position_log, zone_size):
    positions_list = list(i[0] for i in position_log)
    if max(zone_size) < 20:
        print("Rover Planned Trip Map")
        for y in range(zone_size[0], 0, -1):
            p = "{0: >2} ".format(y)
            for x in range(1, zone_size[1] + 1, 1):
                # Final position must take precedence.
                if [x, y] == positions_list[-1]:
                    p += "  {}  ".format(orientation_to_direction(position_log[-1][1]))
                # Then map initial position
                elif [x, y] == positions_list[0]:
                    p += "  *  "
                # Then everything else
                elif [x, y] in positions_list:
                    p += "  #  "
                else:
                    p += "====="
            print(p)
        p = "  "
        for x in range(1, zone_size[1] + 1, 1):
            p += "  {0: >2} ".format(x)
        print(p)

        print("")
        print("Legend:")
        print("  [N, S, E, W] - Orientation and Final Position")
        print("  *            - Initial Position")
        print("  #            - Mapped Area")
        print("  =            - Unmapped Area")
    else:
        print("Map too large. Not printing.")


def validate_rover_in_zone(position, zone_size):
    in_zone = True
    if not (zone_size[0] >= position[0] >= 1):
        in_zone = False
    if not (zone_size[1] >= position[1] >= 1):
        in_zone = False
    return in_zone


def guidance_system(zone_size, command_list, initial_position, initial_orientation, MissionSafe):
    position = initial_position
    orientation = direction_to_orientation(initial_orientation)
    # Keep log of rover positions
    position_log = []
    position_log.append([position, orientation])

    for command in command_list:
        if command == 'M':
            position = move(position, orientation)
            position_log.append([position, orientation])
        elif command in ['L', 'R']:
            orientation = reorient(orientation, command)
            position_log.append([position, orientation])
        else:
            print("Unrecognized command: '{}'".format(command))
            MissionSafe = (MissionSafe and validate_rover_in_zone(position, zone_size))

    return position_log, MissionSafe


def load_mission(file_name):
    """Did not spend any time here. This is user input. And free range user input
    is very hard to validate. So file needs to be exactly right, otherwise we abort."""
    with open(file_name) as f:
        raw_mission_details = f.readlines()
    mission_details = list(i.strip() for i in raw_mission_details)
    zone_size = list(int(i) for i in mission_details[0].split(" "))
    initial_position = list(int(i) for i in mission_details[1].split(" ")[:2])
    initial_orientation = mission_details[1].split(" ")[-1]
    command_list = mission_details[2]
    return zone_size, initial_position, initial_orientation, command_list

# Get list of current files
files = [f for f in os.listdir('.') if os.path.isfile(f)]
valid_mission_files = []
for f in files:
    if f.split(".")[1] == 'rover':
        valid_mission_files.append(f)
valid_mission_files.sort()

valid_numbered_input = list(i + 1 for i in range(len(valid_mission_files)))
print("")
print("Mission Choices:")
for n in valid_numbered_input:
    print("{} - {}".format(n, valid_mission_files[n - 1]))
print("")


try:
    # Python 3
    user_input = input("Please select a mission from above or supply a .rover file: ")
except:
    # Python 2
    user_input = raw_input("Please select a mission from above or supply a .rover file: ")

try:
    mission_file = valid_mission_files[int(user_input) - 1]
except:
    mission_file = user_input

print("")
print("> Loading rover commands\n")
try:
    zone_size, initial_position, initial_orientation, command_list = load_mission(mission_file)
except:
    print("*** Could not load rover commands ***")

try:
    position_log, MissionSafe = guidance_system(zone_size, command_list,
                                                initial_position, initial_orientation, MissionSafe)

    map_area(position_log, zone_size)
    print("")
    print("Final Location: {} {} {}".format(position_log[-1][0][0], position_log[-1][0][1],
                                            orientation_to_direction(position_log[-1][1])))
    print("")
    if MissionSafe:
        print("> Trip is safe, rover does not leave mapped zone.")
        send_commands_to_mars(command_list)
    else:
        print("> Rover trip does not appear safe. Aborting mission.")
except:
    print("Mission experienced a critical failure. Please try turning it off and on again.")

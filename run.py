import json
import sys

from rover import Rover, RoverException


def process_command(rover_command, rover):
    command = rover_command.get('command')
    initial_position = rover_command.get('position')
    rover_id = rover_command.get('rover-id')

    initial_rover_command = initial_position is not None and command == 'new-rover'
    standard_rover_command = rover_id is not None and command is not None

    if initial_position and standard_rover_command:
        raise RoverException('Please only include one of rover_id or position')

    if initial_rover_command:
        initial_x = int(initial_position['x'])
        initial_y = int(initial_position['y'])
        rover.position = rover.home_base = [initial_x, initial_y]

    elif standard_rover_command:
        if command == 'move-forward':
            rover.move()
        else:
            rover.turn_direction(command)

    return rover.output


def process_commands(commands):
    rover_id = None
    try:
        rover_id = commands[1]['rover-id']
    except KeyError:
        rover_id = '1AFC'  # default rover name if none available
    except IndexError:
        pass

    rover = Rover(0, 0, rover_name=rover_id)

    logs_from_rover = []

    for command in commands:
        output = process_command(command, rover)
        logs_from_rover.append(output)

    return logs_from_rover


def main():
    args = sys.argv
    try:
        filename = args[1]
    except IndexError:
        raise IndexError('Please provide filename. i.e. "python run.py my_file.txt"')
    lines_to_pass = []

    try:
        with open(filename, 'r') as fh:
            for line in fh:
                formatted_line = json.loads(line)
                lines_to_pass.append(formatted_line)
    except FileNotFoundError:
        raise

    lines_to_write = process_commands(lines_to_pass)

    with open('rover_log.txt', 'w+') as fh:
        for line in lines_to_write:
            fh.write(json.dumps(line) + '\n')


if __name__ == "__main__":
    main()

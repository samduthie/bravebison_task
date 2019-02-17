import json
import sys


class RoverException(Exception):
    pass


class Rover(object):
    def __init__(self, x, y, identifier='1AFC'):
        self.position = [0, 0]
        self.directions = ['north', 'east', 'south', 'west']
        self.direction_index = 0
        self.fuel_gauge = 20

        #  the first response must give the rover_id although the rover_id is not known in the first example command
        #  because of this, it is auto-set and then allowed to be overwritten
        self.identifier = identifier

    def go_north(self):
        self.position[1] += 1

    def go_south(self):
        self.position[1] -= 1

    def go_east(self):
        self.position[0] += 1

    def go_west(self):
        self.position[0] -= 1

    @property
    def fuel_exists(self):
        if self.fuel_gauge > 0:
            return True
        else:
            return False

    def turn_left(self):
        if self.direction_index == 0:
            self.direction_index = len(self.directions)
        self.direction_index -= 1

    def turn_right(self):
        if self.direction_index == 3:
            self.direction_index = -1
        self.direction_index += 1

    def use_fuel(self):
        if self.fuel_gauge > 0:
            self.fuel_gauge -= 1

    @property
    def direction(self):
        return self.directions[self.direction_index]

    def turn_direction(self, direction_to_move):
        if self.fuel_exists and direction_to_move == 'turn-right':
            self.turn_right()
        elif self.fuel_exists and direction_to_move == 'turn-left':
            self.turn_left()
        else:
            raise RoverException('Please only pass in turn-left or turn-right as directional commands')

        self.use_fuel()

    def move(self):
        if self.fuel_exists and self.direction == 'north':
            self.go_north()
        if self.fuel_exists and self.direction == 'south':
            self.go_south()
        if self.fuel_exists and self.direction == 'west':
            self.go_west()
        if self.fuel_exists and self.direction == 'east':
            self.go_east()

        self.use_fuel()

    def output(self):
        return {
            "rover-id": self.identifier,
            "position": {
                "x": self.position[0],
                "y": self.position[1]
            },
            "direction": self.direction
        }


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
        rover.position = [initial_x, initial_y]

    elif standard_rover_command:
        if command == 'move-forward':
            rover.move()
        else:
            rover.turn_direction(command)

    return rover.output()


def process_commands(commands):
    rover = Rover(0, 0)

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

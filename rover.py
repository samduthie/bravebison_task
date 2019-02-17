from constants import MAX_FUEL


class RoverException(Exception):
    pass


class Rover(object):
    def __init__(self, x, y, rover_name='1AFC'):
        self.position = [x, y]
        self.home_base = [x, y]
        self.directions = ['north', 'east', 'south', 'west']
        self.direction_index = 0
        self.fuel_gauge = MAX_FUEL

        #  the first response must give the rover_id although the rover_id is not known in the first example command
        #  because of this, it is auto-set and then allowed to be overwritten
        self.rover_name = rover_name

    @property
    def fuel_exists(self):
        if self.fuel_gauge > 0:
            return True
        else:
            return False

    @property
    def direction(self):
        return self.directions[self.direction_index]

    def go_north(self):
        self.position[1] += 1

    def go_south(self):
        self.position[1] -= 1

    def go_east(self):
        self.position[0] += 1

    def go_west(self):
        self.position[0] -= 1

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

    def turn_direction(self, direction_to_move):
        if self.fuel_exists and direction_to_move == 'turn-right':
            self.turn_right()
        elif self.fuel_exists and direction_to_move == 'turn-left':
            self.turn_left()
        else:
            raise RoverException('Please only pass in turn-left or turn-right as directional commands')

        self.use_fuel()

    def move(self):
        x = self.position[0]
        y = self.position[1]

        if self.fuel_exists and self.direction == 'north':
            if self.can_reach_home(x, y + 1):
                self.go_north()

        if self.fuel_exists and self.direction == 'south':
            if self.can_reach_home(x, y - 1):
                self.go_south()
        if self.fuel_exists and self.direction == 'west':
            if self.can_reach_home(x - 1, y):
                self.go_west()
        if self.fuel_exists and self.direction == 'east':
            if self.can_reach_home(x + 1, y):
                self.go_east()

        self.use_fuel()

    def distance_from_point_to_home(self, x, y):
        diff_x = x - self.home_base[0]
        diff_y = y - self.home_base[1]
        return [diff_x, diff_y]

    def can_reach_home(self, x, y):
        coords_to_home = self.distance_from_point_to_home(x, y)

        # get the directions that we need to go in
        if coords_to_home[0] > 0:
            x_direction_to_go = 'east'
        elif coords_to_home[0] < 0:
            x_direction_to_go = 'west'
        else:
            x_direction_to_go = ''
        if coords_to_home[1] > 0:
            y_direction_to_go = 'north'
        elif coords_to_home[1] < 0:
            y_direction_to_go = 'south'
        else:
            y_direction_to_go = ''

        # get number of turns we need to change direction
        # if direction_to_go is the same as current direction then turns is 1. otherwise 2
        try:
            x_direction_turns = abs(self.directions.index(x_direction_to_go) - self.direction_index)
        except ValueError:
            x_direction_turns = 0

        if x_direction_turns == 3:
            x_direction_turns = 1  # 1 direction away from where we want to be

        try:
            y_direction_turns = abs(self.directions.index(y_direction_to_go) - self.direction_index)
        except ValueError:
            y_direction_turns = 0

        if y_direction_turns == 3:
            y_direction_turns = 1  # 1 direction away from where we want to be

        if x_direction_to_go == '':
            turns = y_direction_turns
        elif y_direction_to_go == '':
            turns = x_direction_turns
        else:
            turns = max(x_direction_turns, y_direction_turns)

        number_of_commands_to_get_home = coords_to_home[0] + coords_to_home[1] + turns

        enough_fuel_go_get_home = number_of_commands_to_get_home <= self.fuel_gauge
        return enough_fuel_go_get_home

    def can_reach_base(self, x, y):
        return self.fuel_gauge > self.position[0] + x and self.fuel_gauge > self.position[1] + y

    @property
    def output(self):
        return {
            "rover-id": self.rover_name,
            "position": {
                "x": self.position[0],
                "y": self.position[1]
            },
            "direction": self.direction
        }

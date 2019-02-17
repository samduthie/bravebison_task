import unittest

from rover import Rover


class RoverTests(unittest.TestCase):

    def test_rover_can_cycle_through_directions(self):
        rover = Rover(0, 0)
        rover.turn_right()
        self.assertEqual(rover.direction, 'east')

    def test_rover_can_cycle_twice_through_directions(self):
        rover = Rover(0, 0)
        rover.turn_right()
        rover.turn_right()
        self.assertEqual(rover.direction, 'south')

    def test_rover_can_cycle_full_turns_through_direction(self):
        rover = Rover(0, 0)
        for _ in range(8):
            rover.turn_right()
        self.assertEqual(rover.direction, 'north')

    def test_rover_can_cycle_backwards_through_directions(self):
        rover = Rover(0, 0)
        rover.turn_left()
        self.assertEqual(rover.direction, 'west')

    def test_rover_can_cycle_backwards_twice_through_directions(self):
        rover = Rover(0, 0)
        rover.turn_left()
        rover.turn_left()
        self.assertEqual(rover.direction, 'south')

    def test_rover_can_cycle_full_turns_backwards_through_direction(self):
        rover = Rover(0, 0)
        for _ in range(8):
            rover.turn_left()
        self.assertEqual(rover.direction, 'north')

    def test_rover_can_go_into_negative_x_position(self):
        rover = Rover(0, 0)
        rover.go_west()
        self.assertEqual(rover.position, [-1, 0])

    def test_rover_can_go_into_negative_y_position(self):
        rover = Rover(0, 0)
        rover.go_south()
        self.assertEqual(rover.position, [0, -1])

    def test_rover_moves_correctly_north(self):
        rover = Rover(0, 0)
        rover.move()
        self.assertEqual(rover.position, [0, 1])

    def test_rover_moves_correctly_south(self):
        rover = Rover(0, 0)
        rover.turn_right()
        rover.turn_right()
        rover.move()
        self.assertEqual(rover.position, [0, -1])

    def test_rover_moves_correctly_east(self):
        rover = Rover(0, 0)
        rover.turn_right()
        rover.move()
        self.assertEqual(rover.position, [1, 0])

    def test_rover_moves_correctly_west(self):
        rover = Rover(0, 0)
        rover.turn_left()
        rover.move()
        self.assertEqual(rover.position, [-1, 0])

    def test_rover_lowers_fuel_gauge_from_20(self):
        rover = Rover(0, 0)
        rover.move()
        self.assertEqual(rover.fuel_gauge, 19)

    def test_rover_lowers_fuel_gauge_to_0(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 1
        rover.move()
        self.assertEqual(rover.fuel_gauge, 0)

    def test_rover_fuel_gauge_cannot_go_lower_than_0(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 0
        rover.move()
        self.assertEqual(rover.fuel_gauge, 0)

    def test_rover_does_not_mmove_if_fuel_gauage_is_empty(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 0
        rover.move()
        self.assertEqual(rover.position, [0, 0])

    def test_rover_reports_fuel_gauge_is_empty(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 0
        rover.move()
        self.assertFalse(rover.fuel_exists)

    def test_rover_does_not_report_fuel_gauge_is_empty_if_it_has_fuel(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 1
        rover.move()
        self.assertFalse(rover.fuel_exists)

    def test_rover_can_go_north_20_times_and_report_correct_output(self):
        rover = Rover(0, 0)
        for _ in range(20):
            rover.go_north()

        output = rover.output
        expected_output = {
            "x": 0,
            "y": 20
        }

        self.assertEqual(output['position'], expected_output)

    def test_rover_can_go_south_20_times_and_report_correct_output(self):
        rover = Rover(0, 0)
        for _ in range(20):
            rover.go_south()

        output = rover.output
        expected_output = {
            "x": 0,
            "y": -20
        }

        self.assertEqual(output['position'], expected_output)

    def test_rover_can_go_east_20_times_and_report_correct_output(self):
        rover = Rover(0, 0)
        for _ in range(20):
            rover.go_east()

        output = rover.output
        expected_output = {
            "x": 20,
            "y": 0
        }

        self.assertEqual(output['position'], expected_output)

    def test_rover_can_go_west_20_times_and_report_correct_output(self):
        rover = Rover(0, 0)
        for _ in range(20):
            rover.go_west()

        output = rover.output
        expected_output = {
            "x": -20,
            "y": 0
        }

        self.assertEqual(output['position'], expected_output)

    def test_rover_can_go_north_21_times_and_report_correct_output(self):
        rover = Rover(0, 0)
        for _ in range(20):
            rover.go_north()

        output = rover.output
        expected_output = {
            "x": 0,
            "y": 20
        }

        self.assertEqual(output['position'], expected_output)

    def test_rover_can_go_south_21_times_and_report_correct_output(self):
        rover = Rover(0, 0)
        for _ in range(20):
            rover.go_south()

        output = rover.output
        expected_output = {
            "x": 0,
            "y": -20
        }
        self.assertEqual(output['position'], expected_output)

    def test_rover_can_go_east_21_times_and_report_correct_output(self):
        rover = Rover(0, 0)
        for _ in range(20):
            rover.go_east()

        output = rover.output
        expected_output = {
            "x": 20,
            "y": 0
        }
        self.assertEqual(output['position'], expected_output)

    def test_rover_can_go_west_21_times_and_report_correct_output(self):
        rover = Rover(0, 0)
        for _ in range(20):
            rover.go_west()

        output = rover.output
        expected_output = {
            "x": -20,
            "y": 0
        }
        self.assertEqual(output['position'], expected_output)

    def test_rover_can_reach_home_from_base(self):
        rover = Rover(0, 0)
        self.assertTrue(rover.can_reach_home(1, 1))

    def test_rover_can_reach_home_with_enough_fuel(self):
        rover = Rover(5, 5)
        self.assertTrue(rover.can_reach_home(10, 10))

    def test_rover_cant_reach_home_without_fuel(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 0
        self.assertFalse(rover.can_reach_home(10, 10))

    def test_rover_can_reach_home_with_fuel_when_turning_once(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 3
        rover.direction_index = 0  # north
        self.assertTrue(rover.can_reach_home(1, 1))

    def test_rover_cant_reach_home_without_sufficient_fuel_when_turning_once(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 2
        rover.direction_index = 0  # north
        self.assertFalse(rover.can_reach_home(1, 1))

    def test_rover_can_reach_home_with_fuel_when_turning_twice(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 4
        rover.direction_index = 3  # west
        self.assertTrue(rover.can_reach_home(1, 1))

    def test_rover_cant_reach_home_without_sufficient_fuel_when_turning_twice(self):
        rover = Rover(0, 0)
        rover.fuel_gauge = 3
        rover.direction_index = 3 # west
        self.assertFalse(rover.can_reach_home(1, 1))


if __name__ == '__main__':
    unittest.main()

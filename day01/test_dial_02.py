import unittest

from dial_02 import count_rotations


class TestCountRotations(unittest.TestCase):
    def test_no_rotations_within_single_dial(self):
        """Test movement that stays within 0-99 range."""
        lines = ["R10", "L5"]
        result = count_rotations(50, lines)
        self.assertEqual(result, 0)

    def test_single_clockwise_rotation(self):
        """Test a single full rotation clockwise."""
        lines = ["R100"]
        result = count_rotations(50, lines)
        self.assertEqual(result, 1)

    def test_single_counterclockwise_rotation(self):
        """Test a single full rotation counterclockwise."""
        lines = ["L100"]
        result = count_rotations(50, lines)
        self.assertEqual(result, 1)

    def test_multiple_rotations_clockwise(self):
        """Test multiple rotations in one move."""
        lines = ["R250"]
        result = count_rotations(50, lines)
        self.assertEqual(result, 3)

    def test_multiple_rotations_counterclockwise(self):
        """Test multiple counterclockwise rotations."""
        lines = ["L300"]
        result = count_rotations(50, lines)
        self.assertEqual(result, 3)

    def test_crossing_zero_from_below(self):
        """Test crossing zero from position 50 going left."""
        lines = ["L50"]
        result = count_rotations(50, lines)
        self.assertEqual(result, 1)

    def test_crossing_zero_from_above(self):
        """Test crossing zero from right side."""
        lines = ["R50"]
        result = count_rotations(50, lines)
        self.assertEqual(result, 1)

    def test_example_from_terminal(self):
        """Test the example used in terminal: L50 then R300."""
        lines = ["L50", "R300"]
        result = count_rotations(50, lines)
        self.assertEqual(result, 4)

    def test_zero_movement(self):
        """Test that zero movement doesn't count."""
        lines = ["R0", "L0"]
        result = count_rotations(50, lines)
        self.assertEqual(result, 0)

    def test_complex_sequence(self):
        """Test a complex sequence of moves."""
        lines = ["R60", "L110", "R200"]
        result = count_rotations(50, lines)
        # Start: 50
        # R60 -> 110 -> position 10, rotations 1
        # L110 -> -100 -> position 0, rotations 2 (1 + 1 for crossing zero)
        # R200 -> 200 -> position 0, rotations 4 (2 + 1 + 1 for crossing zero)
        self.assertEqual(result, 5)

    def test_empty_lines(self):
        """Test with empty input."""
        lines = []
        result = count_rotations(50, lines)
        self.assertEqual(result, 0)

    def test_position_wraps_correctly(self):
        """Test that position wrapping works correctly."""
        lines = ["R155"]
        result = count_rotations(50, lines)
        # 50 + 155 = 205 -> position 5, rotations 2
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()

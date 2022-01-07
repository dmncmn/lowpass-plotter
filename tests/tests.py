
import unittest


class TestFilter(unittest.TestCase):

    def test_generated_sin_is_2d_vector(self):

        from src.gen import Gen

        gen = Gen()
        gen.sin_ = 100
        x, y = gen.sin_

        self.assertEqual(len(x), len(y))

    def test_filtered_sin_is_2d_vector(self):

        from src.gen import Gen

        gen = Gen()
        x, y = gen._sin_data_filtered

        self.assertEqual(len(x), len(y))

    def test_size_data_and_filtered_data_is_equal(self):

        from src.filter import Filter

        f = Filter()
        f.get_filter = (0.1, 300, 700, 900)
        data = list(range(0, 100))
        filtered_data = f.apply_filter(data)

        self.assertEqual(len(data), len(filtered_data))

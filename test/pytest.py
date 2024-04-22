#importing libraries
import unittest
import cv2
import sys
sys.path.append("PyPaletteAnalyzer/src")
from skin_tone import SkinToneAnalyzer
from color_palette import ColorPalette

class ColorTextTestResult(unittest.TextTestResult):
    COLORS = {
        'pass': '\033[92m',  # green
        'fail': '\033[91m',  # red
        'error': '\033[91m'  # red
    }

    def addSuccess(self, test):
        super().addSuccess(test)

    def addError(self, test, err):
        super().addError(test, err)

    def addFailure(self, test, err):
        super().addFailure(test, err)

class TestColorPalette(unittest.TestCase):
    def setUp(self):
        self.palette_generator = ColorPalette()

    def lines_add(self, message_t):
        print("\n" + "-" * 80 + "\n")
        t1 = "\033[95m\u001B[3m" + message_t + " \u001B[0m"  # Purple color
        lt_1 = "\033[1m" + t1 + "\033[0m"  # Increase size
        c_text_1 = lt_1.center(80)
        print(c_text_1)

    def assert_equal(self, result, expected, message):
        """
        Compares the pass/Fail message and then prints the result
        """
        if result == expected:
            print(f"\033[92m{message} Passed.\033[0m")
        else:
            print(f"\033[91m{message} Failed\033[0m")
            self.failed_test_cases += 1

    def test_get_palette(self):
        """
        does: Test the get_palette method for various undertones.
        
        Test Case 1: Test for 'cool' undertone
        Test Case 2: Test for 'warm' undertone
        Test Case 3: Test for 'neutral' undertone
        """
        # Test for 'cool' undertone
        self.lines_add("Testing Get Palette Function")
        cool_palette = self.palette_generator.get_palette([86.1, -0.8, -0.5])
        self.assert_equal(len(cool_palette), 10, "Test Case 1")
                # Test for 'warm' undertone
        warm_palette = self.palette_generator.get_palette([75.9, 14.5, 20.2])
        self.assert_equal(len(warm_palette), 10, "Test Case 2")
                # Test for 'neutral' undertone
        neutral_palette = self.palette_generator.get_palette([79.7, 6.2, 11.9])
        self.assert_equal(len(neutral_palette), 10, "Test Case 3")


    def test_classify_undertone(self):
        """
        Test the classify_undertone method for various skin tones.

        Test Case 1: Test for 'cool' undertone
        Test Case 2: Test for 'warm' undertone
        Test Case 3: Test for 'neutral' undertone
        """
        # Test for 'cool' undertone
        self.lines_add("Testing Get Classify Function")
        cool_undertone = self.palette_generator.classify_undertone([86.1, -0.8, -0.5])
        self.assert_equal(cool_undertone, "cool", "Test Case 1")

        # Test for 'warm' undertone
        warm_undertone = self.palette_generator.classify_undertone([75.9, 14.5, 20.2])
        self.assert_equal(warm_undertone, "warm", "Test Case 2")

        # Test for 'neutral' undertone
        neutral_undertone = self.palette_generator.classify_undertone([79.7, 6.2, 11.9])
        self.assert_equal(neutral_undertone, "neutral", "Test Case 3")


    def test_delta_e_cie2000(self):
        """
        Test delta_e_cie2000 method for color difference calculation.

        Test Case 1: Test for identical colors
        Test Case 2: Test for non-numeric input
        """
        self.lines_add("Testing Get Delta Function")

        # Test for identical colors
        delta_e = self.palette_generator.delta_e_cie2000([50, 0, 0], [50, 0, 0])
        self.assert_equal(delta_e, 0, "Test Case 1")

        # Test for non-numeric input
        delta_e_not_numeric = self.palette_generator.delta_e_cie2000("invalid_input", [50, 0, 0])
        self.assert_equal(delta_e_not_numeric, None, "Test Case 2")


    def test_get_rgb_from_hex(self):
        """
        Test get_rgb_from_hex method for various hex color inputs.

        Test Case 1: Test for valid hex color input
        Test Case 2: Test for None input
        Test Case 3: Test for numeric input
        """
        self.lines_add("Testing Get RGB from hex Function")

        # Test for valid hex color input
        rgb = self.palette_generator.get_rgb_from_hex("#FFFFFF")
        self.assert_equal(rgb, (255, 255, 255), "Test Case 1")

        # Test for None input
        rgb_none = self.palette_generator.get_rgb_from_hex(None)
        self.assert_equal(rgb_none, None, "Test Case 2")

        # Test for numeric input
        rgb_number = self.palette_generator.get_rgb_from_hex(123)
        self.assert_equal(rgb_number, None, "Test Case 3")



class TestSkinToneAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SkinToneAnalyzer()

    def lines_add(self, message_t):
        print("\n" + "-" * 80 + "\n")
        t1 = "\033[95m\u001B[3m" + message_t + " \u001B[0m"  # Purple color
        lt_1 = "\033[1m" + t1 + "\033[0m"  # Increase size
        c_text_1 = lt_1.center(80)
        print(c_text_1)

    def assert_equal(self, result, expected, message):
        """
        Compares the pass/Fail message and then prints the result
        """
        if result == expected:
            print(f"\033[92m{message} Passed.\033[0m")
        else:
            print(f"\033[91m{message} Failed\033[0m")
            self.failed_test_cases += 1

    def test_get_skin_tone(self):
        """
        Test get_skin_tone method for extracting skin tone from images.

        Test Case 1: Test when faces are detected in the image
        Test Case 2: Test when no faces are detected in the image
        """
        self.lines_add("Testing Get Skin Function")
        image_with_faces = cv2.imread("PyPaletteAnalyzer/test/test_data/sample_1.jpeg")
        skin_tone_with_faces = self.analyzer.get_skin_tone(image_with_faces)
        self.assert_equal(skin_tone_with_faces is not None, True, "Test Case 1")       

        # Test case 2: When no faces are detected in the image
        image_without_faces = cv2.imread("PyPaletteAnalyzer/test/test_data/sample_3.jpg")
        skin_tone_without_faces = self.analyzer.get_skin_tone(image_without_faces)
        self.assert_equal(skin_tone_without_faces is None, True, "Test Case 2")


if __name__ == "__main__":
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=ColorTextTestResult), buffer=False)
import cv2
from src.skin_tone import SkinToneAnalyzer
from src.color_palette import ColorPalette

class MultipleFacesDetectedError(Exception):
    """Exception raised when more than one face is detected in the image."""
    pass

def analyze_image(image_path):
    """
    Analyzes the image to predict skin tone and recommend a color palette.
    Args:
        image_path (str): The path to the image file.
    Returns:
        str: The hexadecimal color code.
    """
    try:
        image = cv2.imread(image_path)
        skin_tone_analyzer = SkinToneAnalyzer()
        try:
            faces = skin_tone_analyzer.detect_faces(image)
            if len(faces) != 1:
                raise MultipleFacesDetectedError("No face or more than one face detected.")
        except Exception as e:
            raise e
        
        try:
            skin_tone = skin_tone_analyzer.get_skin_tone(image)
            if skin_tone is None:
                print("No face detected in the image.")
                return None
        except Exception as e:
            raise e

        palette_generator = ColorPalette()
        under_tone = palette_generator.classify_undertone(skin_tone)
        print("Predicted Skin Tone:", str.upper(under_tone))
        palette = palette_generator.get_palette(skin_tone)
        print("Recommended Color Palette:")
        color_names = palette_generator.get_color_names()
        for color_hex, color_name in color_names.items():
            if color_hex in palette:
                print(f"{color_name}: {color_hex}")

        palette_generator.display_palette(palette)
        return None  # Or return the color_hex if needed
    except MultipleFacesDetectedError as e:
        print("Error:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

analyze_image("path to image")

import cv2
from src.skin_tone import SkinToneAnalyzer
from src.color_palette import ColorPalette

# Load an image
image = cv2.imread("path/to/image.jpeg")

# Analyze the skin tone
skin_tone_analyzer = SkinToneAnalyzer()
skin_tone = skin_tone_analyzer.get_skin_tone(image)

if skin_tone is not None:
    # Generate a color palette
    palette_generator = ColorPalette()
    under_tone = palette_generator.classify_undertone(skin_tone)
    print("Predicted Skin Tone:", under_tone)
    palette = palette_generator.get_palette(skin_tone)
    print("Recommended Color Palette:")
    for color in palette:
        print(color)

    # Display the color palette
    palette_generator.display_palette(palette)
else:
    print("No face detected in the image.")
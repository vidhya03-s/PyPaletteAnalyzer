# PyPaletteAnalyzer

PyPaletteAnalyzer is a Python package that analyzes the skin tone of individuals in an image and provides a recommended color palette based on the detected undertone (cool, warm, or neutral). This package aims to assist users in selecting complementary color palettes that can be applied in various areas, such as fashion, makeup, or interior design.


## Overview
- [Features](#features)
- [Proposed Design and Implementation](#design)
- [Installation Guide](#installation)
- [Example Usage](#usage)
- [Conclusion](#conclusion)


## Features <a id='features'></a>

- Detect faces in an input image and extract the dominant skin tone color values.
- Classify the undertone of the skin tone (cool, warm, or neutral) using the CIEDE2000 color difference formula.
- Provide a predefined color palette based on the classified undertone.
- Display the recommended color palette visually.


## Proposed Design and Implementation <a id='design'></a>

The PyPaletteAnalyzer package comprises two main classes: 
    - SkinToneAnalyzer
    - ColorPalette

<b>SkinToneAnalyzer Class:</b> Detects faces in an image and extracts dominant skin tone color values. It employs OpenCV's Haar Cascade classifiers for face detection and performs the following steps:

- Detect faces using a pre-trained Haar Cascade classifier.
- Extract the region of interest (ROI) containing the face.
- Convert ROI from BGR to RGB color space.
- Further convert RGB values to the LAB color space for perceptual uniformity.
- Collect LAB color values representing skin pixels.
- Apply K-Means clustering to identify the dominant skin tone cluster.
- Return the centroid (average) of the dominant skin tone cluster.

<b>ColorPalette Class:</b> Classifies the undertone of the input skin tone and provides a corresponding color palette. Key components include:

- <i>Predefined Color Palettes:</i> Lists of hexadecimal color codes for cool, warm, and neutral undertones.
- <i>classify_undertone Method:</i> Compares input skin tone LAB color values with reference values using the CIEDE2000 color difference formula to classify the undertone.
- <i>get_palette Method:</i> Returns the corresponding predefined color palette for the classified undertone.

CIEDE2000 is utilized for accurate color difference quantification, considering factors like hue, chroma, and lightness.

By integrating SkinToneAnalyzer and ColorPalette classes, the package can analyze images, extract dominant skin tones, classify undertones, and recommend personalized color palettes.


## Installation Guide <a id='installation'></a>

1. Clone the repository:

```bash
git clone https://github.com/vidhya03-s/PyPaletteAnalyzer.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```


## Example Usage <a id='usage'></a>

```python
#Import required modules
import cv2
from src.skin_tone import SkinToneAnalyzer
from src.color_palette import ColorPalette

# Load an image
image = cv2.imread("path/to/image.jpg")

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
    print("No face detected in the image.")
```


## Conclusion <a id='conclusion'></a>

PyPaletteAnalyzer revolutionizes color palette recommendations by tailoring suggestions to individual skin tones, ensuring harmonious and aesthetically pleasing combinations. While its innovative approach marks a significant step forward, there's room for improvement. Expanding the palette database, accommodating lighting and skin tone variations, and exploring alternative classification algorithms hold promise for enhancing accuracy and adaptability.

Overall, PyPaletteAnalyzer presents a promising solution for those seeking personalized color guidance in fashion, makeup, or interior design. Its seamless integration of computer vision and color theory empowers users to make informed aesthetic decisions that reflect their unique style and preferences.
# cli.py
import sys
from src.image_analyzer import analyze_image

def parse_args():
    if len(sys.argv) != 2:
        print("Usage: analyze_image <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    analyze_image(image_path)
from setuptools import setup, find_packages

setup(
    name='PyPaletteAnalyzer',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'scikit-learn',
        'colormath',
        'webcolors',
        'matplotlib'
    ],
    entry_points={
    'console_scripts': [
        'analyze_image=src.main:analyze_image',
    ],
    },
    author='Team 8',
    author_email='your@email.com',
    description='Skin Tone Analysis and Color Palette Generation package: Analyzes skin tone in images and recommends complementary color palettes based on undertones',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vidhya03-s/PyPaletteAnalyzer.git',
    license='NEU',
)
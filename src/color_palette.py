import numpy as np
import webcolors
import math



class ColorPalette:
    def __init__(self):
        self.color_palettes = {
            "cool": ["#B3C6D9", "#9FB1C4", "#8496AD", "#677C8F", "#516170", "#A4C2D6", "#8BA9C0", "#7290AC", "#596F88", "#415964"],
            "warm": ["#F7D7C3", "#EECAB0", "#E4BC9D", "#D8AB8A", "#CCA077", "#F5D0B5", "#ECC19B", "#E2B282", "#D7A06A", "#CCA051"],
            "neutral": ["#E8E4D9", "#D8D2C4", "#C8C0AF", "#B8B09A", "#A8A085", "#E0DAD0", "#D0C8BB", "#C0B6A6", "#B0A491", "#A0927C"]
        }

    def get_palette(self, skin_tone):
        undertone = self.classify_undertone(skin_tone)
        return self.color_palettes[undertone]

    def classify_undertone(self, skin_tone):
        cool_ref = np.array([86.1, -0.8, -0.5])
        warm_ref = np.array([75.9, 14.5, 20.2])
        neutral_ref = np.array([79.7, 6.2, 11.9])

        cool_diff = self.delta_e_cie2000(skin_tone, cool_ref)
        warm_diff = self.delta_e_cie2000(skin_tone, warm_ref)
        neutral_diff = self.delta_e_cie2000(skin_tone, neutral_ref)

        min_diff = min(cool_diff, warm_diff, neutral_diff)

        if min_diff == cool_diff:
            return "cool"
        elif min_diff == warm_diff:
            return "warm"
        else:
            return "neutral"

    def delta_e_cie2000(self, lab1, lab2):
        """
        Calculates the CIEDE2000 color difference between two Lab colors.
        """
        # Convert Lab values to numpy arrays
        lab1 = np.array(lab1)
        lab2 = np.array(lab2)

        # Calculate C1, C2, and C_bar
        C1 = np.sqrt(lab1[1] ** 2 + lab1[2] ** 2)
        C2 = np.sqrt(lab2[1] ** 2 + lab2[2] ** 2)
        C_bar = (C1 + C2) / 2

        # Calculate G
        G = 0.5 * (1 - np.sqrt(C_bar ** 7 / (C_bar ** 7 + 25 ** 7)))

        # Calculate a1_prime and a2_prime
        a1_prime = (1 + G) * lab1[1]
        a2_prime = (1 + G) * lab2[1]

        # Calculate C1_prime and C2_prime
        C1_prime = np.sqrt(a1_prime ** 2 + lab1[2] ** 2)
        C2_prime = np.sqrt(a2_prime ** 2 + lab2[2] ** 2)

        # Calculate C_bar_prime
        C_bar_prime = (C1_prime + C2_prime) / 2

        # Calculate h1_prime and h2_prime
        h1_prime = np.degrees(np.arctan2(lab1[2], a1_prime)) + 360 if lab1[2] >= 0 else np.degrees(np.arctan2(lab1[2], a1_prime))
        h2_prime = np.degrees(np.arctan2(lab2[2], a2_prime)) + 360 if lab2[2] >= 0 else np.degrees(np.arctan2(lab2[2], a2_prime))

        # Calculate delta_h_prime
        delta_h_prime = h2_prime - h1_prime
        if delta_h_prime > 180:
            delta_h_prime -= 360
        elif delta_h_prime < -180:
            delta_h_prime += 360

        # Calculate delta_L_prime, delta_C_prime, and delta_H_prime
        delta_L_prime = lab2[0] - lab1[0]
        delta_C_prime = C2_prime - C1_prime
        delta_H_prime = 2 * np.sqrt(C1_prime * C2_prime) * np.sin(np.radians(delta_h_prime / 2))

        # Calculate L_bar_prime, C_bar_prime_7, and S_L, S_C, S_H
        L_bar_prime = (lab1[0] + lab2[0]) / 2
        C_bar_prime_7 = C_bar_prime ** 7
        S_L = 1 + (0.015 * (L_bar_prime - 50) ** 2) / np.sqrt(20 + (L_bar_prime - 50) ** 2)
        S_C = 1 + 0.045 * C_bar_prime
        h_bar_prime = (h1_prime + h2_prime) / 2
        T = 1 - 0.17 * np.cos(np.radians(h_bar_prime - 30)) + 0.24 * np.cos(np.radians(2 * h_bar_prime)) + 0.32 * np.cos(np.radians(3 * h_bar_prime + 6)) - 0.2 * np.cos(np.radians(4 * h_bar_prime - 63))
        S_H = 1 + 0.015 * C_bar_prime * T

        # Calculate delta_theta and R_T
        delta_theta = 30 * np.exp(-((180 / np.pi * h_bar_prime - 275) / 25) ** 2)
        R_C = 2 * np.sqrt(C_bar_prime_7 / (C_bar_prime_7 + 25 ** 7))
        R_T = -R_C * np.sin(2 * np.radians(delta_theta))

        # Calculate phi_1, phi_2, and phi_bar_prime
        phi_1 = np.sqrt(C1_prime ** 7 / (C1_prime ** 7 + 25 ** 7))
        phi_2 = np.sqrt(C2_prime ** 7 / (C2_prime ** 7 + 25 ** 7))
        phi_bar_prime = phi_1 * phi_2

        # Calculate S_H_bar_prime
        S_H_bar_prime = phi_bar_prime + (1 - phi_bar_prime) * S_C
        delta_L_prime /= S_L
        delta_C_prime /= S_C
        delta_H_prime /= S_H
        C_bar_prime_7 /= (C_bar_prime_7 + 25 ** 7)

        R_T = S_H * R_T

        delta_E = math.sqrt(delta_L_prime ** 2 + delta_C_prime ** 2 + delta_H_prime ** 2 + R_T * delta_C_prime * delta_H_prime)

        return delta_E
    
    
    def get_rgb_from_hex(self, hex_color):
        rgb = webcolors.hex_to_rgb(hex_color)
        return rgb

    def display_palette(self, palette):
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
    
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.set_title("Color Palette")
    
        num_colors = len(palette)
        width = 1.0 / num_colors
        for i, color in enumerate(palette):
            rect = patches.Rectangle((i * width, 0), width, 1, facecolor=color, edgecolor='black')
            ax.add_patch(rect)
            ax.text(i * width + width / 2, -0.2, color, ha='center', va='top')
    
        plt.axis('off')
        plt.show()
    

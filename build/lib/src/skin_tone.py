import cv2
import numpy as np
from sklearn.cluster import KMeans


class SkinToneAnalyzer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_faces(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def get_skin_tone(self, image):
        faces = self.detect_faces(image)
        skin_pixels = []

        for (x, y, w, h) in faces:
            face_roi = image[y:y+h, x:x+w]
            face_roi_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
            face_roi_lab = cv2.cvtColor(face_roi_rgb, cv2.COLOR_RGB2LAB)

            skin_pixels.extend(face_roi_lab.reshape(-1, 3))

        if not skin_pixels:
            return None

        skin_pixels = np.array(skin_pixels)
        kmeans = KMeans(n_clusters=3, random_state=0).fit(skin_pixels)
        skin_tone_cluster = kmeans.cluster_centers_[np.argmin(kmeans.inertia_)]

        return skin_tone_cluster
    
#__all__ = ['SkinToneAnalyzer']
"""
Contains classes and tools for object detection.
"""
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
from matplotlib.patches import Rectangle
from PIL import Image
from typing import List


class Detector:
    def __init__(self) -> None:
        self.detector = MTCNN()

    def detect_faces(self, image: str) -> List:
        """
        Returns list of images with faces
        :param image: path to image
        :return list: containing all faces detected.
        """
        image = plt.imread(image)
        return self.detector.detect_faces(image)

    def highlight_faces(self, image: str, faces: List) -> None:
        """
        Draws red rectangles to highlights faces
        :param image: path to image
        :param faces: List that contains faces description
        """
        image = plt.imread(image)
        plt.imshow(image)
        ax = plt.gca()
        for face in faces:
            x, y, width, height = face['box']
            face_border = Rectangle((x, y), width, height,
                                    fill=False, color='red')
            ax.add_patch(face_border)
        plt.show()

    def extract_faces_from_image(self, image: str, faces: List, required_size: tuple=(224, 224)) -> List:
        """
        Extracts faces from image
        :param image: path to image
        :param required_size: image size
        :param faces: List of detected faces
        :return List of PIL.image objects
        """
        image = plt.imread(image)
        face_images = []
        for face in faces:
            x1, y1, width, height = face['box']
            x2, y2 = x1 + width, y1 + height
            face_boundary = image[y1:y2, x1:x2]
            if not face_boundary.any():
                continue
            face_images.append(Image.fromarray(face_boundary))
        return face_images

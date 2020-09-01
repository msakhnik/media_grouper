"""
Class that contains meta information about image.
TBA.
"""
from typing import List, Dict

import PIL.Image
import imquality.brisque as brisque
import datetime
from .media import Media
from .detect import Detector


class Image(Media):
    """
    Contains meta information about image.
    Takes path to image and object with MTCNN initialized
    """
    SUPPORTED_FORMATS = ("jpeg", "jpg", "jpe", "png")

    def __init__(self, path: str, detector: Detector) -> None:
        """
        :param path: path to image
        :param detector: instance that has common method to detect objects on image
        """
        self.path = path
        self.detector = detector

    def find_faces(self) -> List:
        """
        Returns list of faces.
        Each item of the list is a dictionary with the following info:
        'box', 'confidence', 'keypoints', 'nose', 'mouth_left', 'mouth_right'
        :return list of face BBoxes
        """
        return self.detector.detect_faces(self.path)

    def get_exif_data(self) -> Dict:
        """
        Extracts exif data if exists
        return: dictionary with image's exif data
        """
        return PIL.Image.open(self.path)._getexif()

    def get_creation_date(self):
        """
        :return creation datein human readable format
        """
        exif = self.get_exif_data()
        if not exif:
            return None
        return datetime.datetime.strptime(exif[36867], "%Y:%m:%d %H:%M:%S")

    def extract_faces(self, faces) -> List:
        """
        :return path to temporary stored images with extracted faces
        """
        return self.detector.extract_faces_from_image(self.path, faces)

    def get_quality(self, faces) -> int:
        """
        :return max quality of extracted faces
        """
        faces = self.extract_faces(faces)
        if not faces:
            return 0
        quality = 0
        for face in faces:
            quality = max(brisque.score(face), quality)
        return quality

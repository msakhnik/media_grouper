"""
Class that contains meta information about image.
TBA.
"""
import ffmpeg
import datetime
from typing import List, Dict
from .media import Media


class Video(Media):
    """
    Contains meta information about image.
    Takes path to image and object with MTCNN initialized
    """
    SUPPORTED_FORMATS = ("mp4", )

    def __init__(self, path: str, detector: None) -> None:
        """
        :param path: path to video file
        :param detector: instance that has common method to detect objects on video
        """
        self.path = path
        self.detector = detector

    def get_exif_data(self) -> Dict:
        """
        Extracts exif data if exists
        :return dictionary with exif data based on ffmpeg library
        """
        return ffmpeg.probe(self.path)

    def get_creation_date(self) -> str:
        """
        Gets exif data and finds cretional date
        :return creational date in human readable format
        """
        exif = self.get_exif_data()
        if not exif or not exif["format"]["tags"]:
            return None
        return datetime.datetime.strptime(exif["format"]["tags"]["creation_time"],
                                          '%Y-%m-%dT%H:%M:%S.%f%z')

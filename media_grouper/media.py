"""
Abstract class that describes media objects interfaces
"""
from typing import List, Dict


class Media:
    SUPPORTED_FORMATS = tuple()

    def __init__(self, path: str, detector: None) -> None:
        self.path = ""
        self.detector = None

    def find_faces(self) -> List:
        raise NotImplementedError

    def get_exif_data(self) -> Dict:
        raise NotImplementedError

    def get_creation_date(self):
        raise NotImplementedError

    def extract_faces(self, faces) -> List:
        raise NotImplementedError

    def get_quality(self, faces) -> int:
        raise NotImplementedError

    def show_media(self):
        raise NotImplementedError

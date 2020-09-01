import os
import shutil
import sys
import glob
import time
import datetime
import logging
from media_grouper.image import Image
from media_grouper.video import Video
from media_grouper.detect import Detector
from typing import List


class MediaGrouper:
    def __init__(self,
                 src: str,
                 dst: str,
                 prefixes: List,
                 start_date: str,
                 end_date: str,
                 group_by: str) -> None:
        """
        :param src: path to source folder with media data
        :param dst: output folder
        :param prefixes: list with prefixes like timestamp, quality, faces.
        :param start_date: begin date
        :param end_date: end date
        :param group_by: day/month/year
        """
        self.src_folder = src
        self.dst_folder = os.path.abspath(dst)
        self.prefixes = prefixes
        self.date_range = self.get_datetime_range(start_date, end_date)
        self.group_by = group_by

    def create_destination_folder(self, force_rewrite=False) -> None:
        """
        Creates the destination folder.
        :param force_rewrite: enable/disable y/n dialog
        """
        if os.path.exists(self.dst_folder):
            if not force_rewrite:
                if input(("The folder '{}' is not empty. \n"
                          "Press 'y' to delete it: ").format(self.dst_folder)) != "y":
                    sys.exit()
            logging.info("Removed folder: '{}'".format(self.dst_folder))
            shutil.rmtree(self.dst_folder)
        os.makedirs(self.dst_folder)
        logging.info("Created folder: '{}'".format(self.dst_folder))

    def get_new_dst_media_name(self, src_media, _date):
        """
        :param src_media: path to media file
        :param _date: media creation timestamp
        :return new media names with prefixes
        """
        prefix = ""
        if "timestamp" in self.prefixes:
            prefix += "{}_".format(int(time.mktime(_date.timetuple())))
        faces = None
        if "faces" in self.prefixes:
            faces = src_media.find_faces()
            prefix += "{} person(s)_".format(len(faces))
        if "quality" in self.prefixes:
            if faces is None:
                faces = src_media.find_faces()
            quality = src_media.get_quality(faces)
            prefix += "quality: {}_".format(quality)

        return "{}{}".format(prefix, os.path.basename(src_media.path))

    def get_subfolder_name(self, media_date:datetime) -> str:
        """
        Creates subfolder name. Depends on options.order_by
        :param media_date: timestamp
        :return subfoilder name in choices [day/month/year]
        """
        subfolder_name = None
        if self.group_by == "day":
            subfolder_name = media_date.strftime("%Y-%m-%d")
        elif self.group_by == "month":
            subfolder_name = media_date.strftime("%Y-%b")
        else:
            subfolder_name = media_date.strftime("%Y")
        return subfolder_name

    @staticmethod
    def get_datetime_range(start_date, end_date):
        """
        TBA
        """
        if start_date or end_date:
            if not start_date:
                start_date = datetime.datetime.min
            if not end_date:
                end_date = datetime.datetime.now()
        else:
            return None
        return (start_date, end_date)

    def process_media_data(self) -> None:
        """
        Walks throught the source folder and finds all objects
        """
        detector = Detector()
        logging.info("Working...")
        # recursively walks through all files in the source folder
        for filename in glob.iglob(self.src_folder + '**/**', recursive=True):
            # filter files
            if os.path.isdir(filename):
                continue
            _, file_extension = os.path.splitext(filename)
            if file_extension[1:] in Image.SUPPORTED_FORMATS:
                media = Image(filename, detector)
                faces = media.find_faces()
                media.extract_faces(faces)
            elif file_extension[1:] in Video.SUPPORTED_FORMATS:
                media = Video(filename, None)
                media.get_exif_data()
            else:
                logging.warning("Unsupported file format: ", filename)
                continue

            # read creation date from exif data
            media_date = media.get_creation_date()
            # the start/end day options are not required
            if self.date_range is not None:
                if self.date_range[0] <= media_date <= self.date_range[1]:
                    continue
            # add prefix (if exists)
            dst_name = self.get_new_dst_media_name(media, media_date)
            # check if order_by exists and create subfolders
            if self.group_by:
                sub_folder = self.get_subfolder_name(media_date)
                sub_folder_path = os.path.join(self.dst_folder, sub_folder)
                if not os.path.exists(sub_folder_path):
                    os.makedirs(sub_folder_path)
                new_path = os.path.join(sub_folder_path, dst_name)
            else:
                new_path = os.path.join(self.dst_folder, dst_name)
            logging.info("Copied {} -> {}".format(filename, new_path))
            shutil.copy(media.path, new_path)
        logging.info("Done!")

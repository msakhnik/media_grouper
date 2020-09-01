"""
The main module that processes images and creates destination with updated names.
"""
import datetime
import logging
from argparse import ArgumentParser
from media_grouper.media_grouper import MediaGrouper


def main() -> None:
    opt_parser = ArgumentParser()
    opt_parser.add_argument("--source", dest="source", help="Path to folder with images")
    opt_parser.add_argument("--destination", dest="destination", help="Path to output folder")
    # TODO: create a custom class that combines 'choices' and 'nargs'
    opt_parser.add_argument("--prefixes", dest="prefixes", nargs='+',
                            help=(
                                "List of parts that will be added to origin name. "
                                "Allowed value: 'timestamp', 'faces', 'quality'."))
    opt_parser.add_argument("--group_by", dest="group_by", choices=["day", "month", "year"],
                            help="Create subfolders with media files grouped by period: 'day', 'month', 'year'")
    opt_parser.add_argument("--start_date", dest="start_date", type=datetime.datetime.fromisoformat,
                            help="Start of the datetime range")
    opt_parser.add_argument("--end_date", dest="end_date", type=datetime.datetime.fromisoformat,
                            help="Start of the datetime range")
    opt_parser.add_argument("--loglevel", dest="loglevel", default="INFO", choices=["DEBUG",
                                                                                    "INFO",
                                                                                    "WARNING",
                                                                                    "ERROR"
                                                                                    ], help="")

    # TODO: add argument to determine type of copying
    options = opt_parser.parse_args()
    logging.basicConfig(level=options.loglevel)
    media_grouper = MediaGrouper(options.source,
                                 options.destination,
                                 options.prefixes,
                                 options.start_date,
                                 options.end_date,
                                 options.group_by
                                 )
    media_grouper.create_destination_folder()
    media_grouper.process_media_data()


if __name__ == "__main__":
    main()

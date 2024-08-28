from datetime import datetime
from pathlib import Path
import re
import subprocess

import click

from PIL.ExifTags import Base
from PIL import Image


def parse_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")


@click.command()
@click.argument(
    "source", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.argument(
    "destination", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Do not move files, just print them.",
)
def organize(source, destination, dry_run=False):
    src_path = Path(source)
    dest_path = Path(destination)
    if src_path == dest_path:
        raise click.BadParameter("Source and destination paths cannot be the same.")

    for from_file in src_path.iterdir():
        if not from_file.suffix == ".NEF":
            continue

        image = Image.open(from_file)
        exif = image.getexif()

        date_time_str = exif.get(Base.DateTime)
        date_time_original_str = exif.get(Base.DateTimeOriginal)

        datetime_original = parse_datetime(date_time_original_str)
        dir_name = datetime_original.strftime("%Y-%m-%d")
        dir_path = dest_path / dir_name
        if not dir_path.exists():
            dir_path.mkdir()

        to_file = dir_path / from_file.name

        print(f"{from_file} -> {to_file}")

        if not dry_run:
            from_file.rename(to_file)

        # TODO: Copy XMP files as well?
        # TODO: ExifTools Date/Time shift feature should be used.
        # e.g. like that:
        # '2005:01:27 20:30:00'  '6'       +   '2005:01:28 02:30:00'
        # TODO: Remove executable flags


if __name__ == "__main__":
    organize()

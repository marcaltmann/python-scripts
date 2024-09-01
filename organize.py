from datetime import datetime
from pathlib import Path

import click

from PIL.ExifTags import Base
from PIL import Image


def parse_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")


@click.command()
@click.argument("source", type=click.Path(exists=True, file_okay=False, dir_okay=True))
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
@click.option(
    "-x",
    "--xmp-files",
    is_flag=True,
    default=False,
    help="Also move accompanying xmp files.",
)
def organize(source, destination, dry_run=False, xmp_files=False):
    src_path = Path(source)
    dest_path = Path(destination)
    if src_path == dest_path:
        raise click.BadParameter("Source and destination paths cannot be the same.")

    for nef_file in src_path.iterdir():
        if not nef_file.suffix == ".NEF":
            continue

        xmp_file = nef_file.with_suffix(".NEF.xmp")
        has_xmp_file = xmp_file.exists()

        image = Image.open(nef_file)
        exif = image.getexif()

        datetime_original_str = exif.get(Base.DateTimeOriginal)
        datetime_original = parse_datetime(datetime_original_str)

        date_dir_name = datetime_original.strftime("%Y-%m-%d")
        date_dir_path = dest_path / date_dir_name
        if not date_dir_path.exists():
            date_dir_path.mkdir()

        nef_file_new = date_dir_path / nef_file.name
        print(f"{nef_file} -> {nef_file_new}")

        if not dry_run:
            nef_file.rename(nef_file_new)

        if xmp_files and has_xmp_file:
            xmp_file_new = date_dir_path / xmp_file.name
            print(f"{xmp_file} -> {xmp_file_new}")

            if not dry_run:
                xmp_file.rename(xmp_file_new)


if __name__ == "__main__":
    organize()

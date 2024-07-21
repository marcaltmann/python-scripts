from pathlib import Path
import re
import subprocess

import click


@click.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Do not perform renames, just show them.",
)
def rename(directory, dry_run=False):
    path = Path(directory)

    for from_file in path.iterdir():
        if not from_file.is_file():
            continue

        name = from_file.name

        pattern = re.compile(r"^(\d{2,4})(\d{2})(\d{2})_")
        match = pattern.match(name)
        if not match:
            continue

        result = re.sub(pattern, r"\1_\2_\3.", name)
        to_file = from_file.with_name(result)

        cmd = "git mv %s %s" % (from_file.name, to_file.name)

        if dry_run:
            print(cmd)
        else:
            subprocess.run(["git", "mv", from_file.name, to_file.name], cwd=str(path))


if __name__ == "__main__":
    rename()

import locale
from pathlib import Path

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")

path_ext_drive = Path("/media/marc") / "bu_02" / "fotos_2024"
assert path_ext_drive.exists()

# --- all files and dirs ---

# How many files and directories in the entire path?
all_files_dirs = list(path_ext_drive.rglob("*"))
file_count = len(all_files_dirs)

print(
    locale.format_string("%d", file_count, grouping=True),
    "Dateien und Verzeichnisse"
)

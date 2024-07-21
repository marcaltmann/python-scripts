from pathlib import Path
import re
import subprocess

path = Path(__file__).parent

for file in path.iterdir():
    if not file.is_file():
        continue

    name = file.name
    stem = file.stem

    pattern = re.compile(r"(\d{4})(\d{2})(\d{2})_")
    match = pattern.match(name)
    if not match:
        continue

    result = re.sub(pattern, r"\1_\2_\3.", name)
    file2 = file.with_name(result)

    from_path = str(file)
    to_path = str(file2)

    cmd = "/usr/bin/git mv %s %s" % (from_path, to_path)
    #print(cmd)
    subprocess.call(cmd, shell=True)

import argparse
import os
import re
from typing import List, Dict


parser = argparse.ArgumentParser(
    description="Renames all multimedia files in a folder."
)
parser.add_argument(
    "-p",
    "--path",
    type=str,
    required=True,
    help="Absolute path of the folder to organize.",
)
args = parser.parse_args()
EXTENSIONS = (".mp4", ".mkv", ".avi", ".mpg", ".m4v", ".mpeg")


def search_files() -> List[str]:
    """Searches for files with multimedia extensions.

    Args: None.

    Returns: a list of strings.

    """
    try:
        files = [f for f in os.listdir(args.path) if f.endswith(EXTENSIONS)]
        return files
    except OSError as e:
        print(f"Error trying to locate the folder: {e}")
        return {}


def get_chapters_and_extension(files: List[str]) -> Dict[str, List[str]]:
    """Creates a dictionary with every file name as key and a list of
    ["EPISODE", ".FORMAT"] as value.

    Args: files is a list of strings.

    Returns: A dictionary with string keys and Lists of strings as values.

    """
    return {
        f: [
            (
                re.findall(r"E\d{2}", f)[0]
                if re.findall(r"E\d{2}", f)
                else (re.findall(r"Special", f)[0] if re.findall(r"Special", f) else f)
            ),
            re.findall(r"\..+$", f)[0] if re.findall(r"\..+$", f) else f,
        ]
        for f in files
    }


def get_season() -> str:
    """Gets the season of the multimedia.

    Args: None.

    Returns: The season of the multimedia in a string.

    """
    return args.path.split("/")[-1][-2:]


def get_name() -> str:
    """Gets the name of the multimedia.

    Args: None.

    Returns: The name of the multimedia in a string.

    """
    return args.path.split("/")[-2]


def change_filenames(name: str, season: str, files: Dict[str, List[str]]) -> None:
    """Renames every multimedia file on the folder.

    Args: name is a string.
          season is a string of digits.
          files is a dictionary of string keys and list of strings as value.

    Returns: None.

    """
    for original_name, data in files.items():
        new_name = f"{name} {season}{data[0]}{data[1]}"
        if original_name != new_name:
            os.rename(
                os.path.join(args.path, original_name),
                os.path.join(args.path, new_name),
            )
    return None


def main() -> None:
    """Main function of program."""
    files = search_files()
    if not files:
        print("No multimedia files found. Check the PATH.")
        return
    files_ep_ex = get_chapters_and_extension(files)
    season = f"S{get_season()}"
    name = get_name()
    change_filenames(name, season, files_ep_ex)
    return None


if __name__ == "__main__":
    main()

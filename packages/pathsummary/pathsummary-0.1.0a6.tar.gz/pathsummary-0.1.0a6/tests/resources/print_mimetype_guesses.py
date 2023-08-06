"""
This file is just a helper file to print the mime type guesses.
"""
import mimetypes
from dataclasses import field, dataclass
from pathlib import Path
from typing import List, Tuple

import yaml
from doctestprinter import doctest_iter_print


@dataclass
class VideoFormatEntry:
    """
    >>> VideoFormatEntry("Matrosky", ".mkv")
    VideoFormatEntry(name='Matrosky', file_extensions=['.mkv'], container_format='', video_coding_formats='', audio_coding_formats='', notes='')
    >>> VideoFormatEntry("Quicktime", [".mov", ".qt"])
    VideoFormatEntry(name='Quicktime', file_extensions=['.mov', '.qt'], container_format='', video_coding_formats='', audio_coding_formats='', notes='')
    """

    name: str
    file_extensions: List = field(default_factory=list)
    container_format: str = ""
    video_coding_formats: str = ""
    audio_coding_formats: str = ""
    notes: str = ""

    def __post_init__(self):
        if isinstance(self.file_extensions, str):
            self.file_extensions = [self.file_extensions]

    def guess_types(self) -> List[Tuple[str, str]]:
        """

        Returns:

        Examples:
            >>> sample = VideoFormatEntry("Quicktime", [".mov", ".qt"])
            >>> sample.guess_types()
            [('.mov', 'video/quicktime', 'None'), ('.qt', 'video/quicktime', 'None')]
        """
        results = []
        for extension in self.file_extensions:
            mime_type, encoding = mimetypes.guess_type("a{}".format(extension))
            results.append((str(extension), str(mime_type), str(encoding)))
        return results


def _load_video_format_data():
    """
    Prints the mimetype guesses.

    .. doctest::

        >>> from doctestprinter import print_tree
        >>> sample_data = _load_video_format_data()
        >>> print_tree(sample_data[0])
        {.
                            name : Matroska
                 file_extensions : .mkv
                container_format : Matroska
            video_coding_formats : any
            audio_coding_formats : any
                           notes : nan

    """
    folder_of_this_script = Path(__file__).resolve().parent
    target_yaml_filepath = folder_of_this_script.joinpath("video_formats.yml")
    with target_yaml_filepath.open("r") as yaml_file:
        content = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    return content


def _raw_to_entries(raw_content):
    """

    Args:
        raw_content:

    Returns:

    .. doctest::

        >>> entries = _raw_to_entries(_load_video_format_data())
        >>> entries[0]
        VideoFormatEntry(name='Matroska', file_extensions=['.mkv'], container_format='Matroska', video_coding_formats='any', audio_coding_formats='any', notes=nan)

    """
    all_entries = []
    for raw_item in raw_content:
        all_entries.append(VideoFormatEntry(**raw_item))
    return all_entries


def __main__():
    raw_content = _load_video_format_data()
    all_entries = _raw_to_entries(raw_content)
    for entry in all_entries:
        guessed_types = entry.guess_types()
        doctest_iter_print(
            guessed_types,
            edits_item=lambda x: "{: >10}{: >20}{: >10}".format(x[0], x[1], x[2])
        )


if __name__ == "__main__":
    __main__()

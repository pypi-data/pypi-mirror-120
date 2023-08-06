__author__ = "David Scheliga"
__email__ = "david.scheliga@gmx.de"
__version__ = "0.1.0a5"

import click
import mimetypes
from collections import namedtuple
from pathlib import Path
from typing import Union, Tuple, List, Iterator, Optional
import pandas
from doctestprinter import prepare_pandas
from pathwalker import walk_file_paths
from pandas import DataFrame, Series

FileMetaData = namedtuple("FileMetaData", "filepath mimetype")


APath = Union[str, Path]


class FileTypes:
    IMAGE = "image"
    VIDEO = "video"


FILETYPE_IMAGE = "image"
"""
Deprecated; use FileTypes.IMAGE instead.
"""


_OS_INDEPENDENT_MIMETYPE_MAP = {
    "image/x-ms-bmp": "image/bmp",
    "application/xml": "text/xml",
    "video/x-msvideo": "video/avi",
}

_SPECIAL_FORMATS = {
    ".cine": ("video/vision-research-cine", None),
    ".yml": ("text/yaml", None),
    ".yaml": ("text/yaml", None),
    ".md": ("text/markdown", None),
    ".rst": ("text/restructured", None),
}


def _guess_mimetype(file_path: Path) -> Tuple[str, str]:
    """
    Guess the mimetype of the file within the requested path.

    Args:
        file_path:
            Filepath for which the mimetype is requested.

    Returns:
        Tuple[str, str]:
            mimetype, encoding see `python.mimetypes` for more

    Examples:
        >>> from pathsummary import _guess_mimetype
        >>> from pathlib import Path
        >>> mimetype, encoding = _guess_mimetype(Path("filename.bmp"))
        >>> mimetype
        'image/bmp'
        >>> _guess_mimetype(Path("unknown.something"))
        (None, None)
        >>> _guess_mimetype(Path("not_standard.cine"))
        ('video/vision-research-cine', 'None')

    """
    assert isinstance(file_path, Path), "file_path must be type of pathlib.PurePath"
    if file_path.suffix in _SPECIAL_FORMATS:
        mimetype, encoding = _SPECIAL_FORMATS[file_path.suffix]
        return mimetype, str(encoding)
    mimetype, encoding = mimetypes.guess_type(file_path.name)
    if mimetype in _OS_INDEPENDENT_MIMETYPE_MAP:
        return _OS_INDEPENDENT_MIMETYPE_MAP[mimetype], str(encoding)
    return mimetype, encoding


_COLUMN_UNIQUE_COUNTS = "count"
_COLUMN_REL_COUNTS = "ratio"
_COLUMN_ROOTPATH = "file_rootpath"
_COLUMN_FILENAME = "filename"
_COLUMN_MIMETYPE = "mimetype"
_COLUMN_ENCODING = "encoding"
_COLUMN_FILETYPE = "filetype"
_COLUMN_SUBTYPE = "subtype"
_RAW_TABLE_COLUMNS = [
    _COLUMN_ROOTPATH,
    _COLUMN_FILENAME,
    _COLUMN_MIMETYPE,
    _COLUMN_ENCODING,
]

_SELECT_ALL_FILES = "*"


def _make_raw_summary_table(
    iterates_file_paths: Iterator[Path], recursive: bool = False
) -> DataFrame:
    """
    A table containing file's parent path, filename, mimetype and encoding.

    Args:
        folder_path:
        recursive:

    Returns:
        DataFrame

    .. doctest::

        >>> from pathsummary import _make_raw_summary_table
        >>> from pathwalker import walk_file_paths
        >>> from doctestprinter import print_pandas
        >>> file_iterator = walk_file_paths(
        ...             root_path="./tests/resources/images",
        ...             filter_pattern="*",
        ...             recursive=False
        ...         )
        >>> sample_table = _make_raw_summary_table(iterates_file_paths=file_iterator)
        >>> print_pandas(sample_table)
                     file_rootpath      filename    mimetype  encoding
         0  tests/resources/images   image00.bmp   image/bmp      None
         1  tests/resources/images  image00.jpeg  image/jpeg      None
         2  tests/resources/images   image00.jpg  image/jpeg      None
         3  tests/resources/images   image00.png   image/png      None
         4  tests/resources/images   image00.tif  image/tiff      None
         5  tests/resources/images  image00.tiff  image/tiff      None
         6  tests/resources/images   image01.BMP   image/bmp      None
         7  tests/resources/images  image01.JPEG  image/jpeg      None
         8  tests/resources/images   image01.JPG  image/jpeg      None
         9  tests/resources/images   image01.PNG   image/png      None
        10  tests/resources/images   image01.TIF  image/tiff      None
        11  tests/resources/images  image01.TIFF  image/tiff      None

    """
    raw_table_entries = []
    for filepath in iterates_file_paths:
        mimetype, encoding = _guess_mimetype(filepath)
        raw_table_entries.append((filepath.parent, filepath.name, mimetype, encoding))
    return DataFrame(raw_table_entries, columns=_RAW_TABLE_COLUMNS)


def _make_raw_summary_table_from_path(
    root_path: Path, recursive: bool = False
) -> DataFrame:
    """
    A table containing file's parent path, filename, mimetype and encoding.

    Args:
        root_path:
        recursive:

    Returns:
        DataFrame
    """
    raw_table_entries = []
    for filepath in walk_file_paths(
        root_path=root_path, filter_pattern=_SELECT_ALL_FILES, recursive=recursive
    ):
        mimetype, encoding = _guess_mimetype(filepath)
        raw_table_entries.append((filepath.parent, filepath.name, mimetype, encoding))
    return DataFrame(raw_table_entries, columns=_RAW_TABLE_COLUMNS)


def _split_mimetype_of_summary_table(raw_table: DataFrame) -> DataFrame:
    """

    Args:
        raw_table:

    Returns:

    """
    assert not raw_table.empty, "This method cannot handle empty tables."
    mimetype_column = raw_table.loc[:, _COLUMN_MIMETYPE]

    mimetype_column[mimetype_column.isna()] = "unknown/unknown"

    category_and_type = mimetype_column.str.split(pat="/", expand=True)
    category_and_type.columns = [_COLUMN_FILETYPE, _COLUMN_SUBTYPE]
    columns_without_mimetype = _RAW_TABLE_COLUMNS.copy()
    columns_without_mimetype.remove(_COLUMN_MIMETYPE)
    table_without_mimetype = raw_table[columns_without_mimetype]
    return pandas.concat([table_without_mimetype, category_and_type], axis=1)


def _make_empty_table() -> DataFrame:
    """
    Makes an empty path summary table.

    Returns:
        DataFrame

    .. doctest::

        >>> sample_table = _make_empty_table()
        >>> sample_table
        Empty DataFrame
        Columns: [file_rootpath, filename, encoding]
        Index: []
        >>> sample_table.loc[('video', 'avi'),:] = ["/a", "path.avi", None]
        >>> from doctestprinter import print_pandas
        >>> print_pandas(sample_table)
                           file_rootpath  filename  encoding
        filetype  subtype
           video      avi             /a  path.avi      None
    """
    empty_multi_index = pandas.MultiIndex(
        levels=[[], []], codes=[[], []], names=[_COLUMN_FILETYPE, _COLUMN_SUBTYPE]
    )

    _empty_table_columns = [
        _COLUMN_ROOTPATH,
        _COLUMN_FILENAME,
        _COLUMN_ENCODING,
    ]
    return DataFrame(index=empty_multi_index, columns=_empty_table_columns)


def _make_path_summary(iterates_file_paths) -> DataFrame:
    """

    Args:
        folder_path:

    Returns:

    Examples:
        >>> from pathsummary import summarize_folder_files
        >>> from doctestprinter import print_pandas
        >>> sample_summary = summarize_folder_files("tests/resources/images")
        >>> print_pandas(sample_summary)
                                    file_rootpath      filename  encoding
        filetype  subtype
           image      bmp  tests/resources/images   image00.bmp      None
                      bmp  tests/resources/images   image01.BMP      None
                     jpeg  tests/resources/images  image00.jpeg      None
                     jpeg  tests/resources/images   image00.jpg      None
                     jpeg  tests/resources/images  image01.JPEG      None
                     jpeg  tests/resources/images   image01.JPG      None
                      png  tests/resources/images   image00.png      None
                      png  tests/resources/images   image01.PNG      None
                     tiff  tests/resources/images   image00.tif      None
                     tiff  tests/resources/images  image00.tiff      None
                     tiff  tests/resources/images   image01.TIF      None
                     tiff  tests/resources/images  image01.TIFF      None

        >>> sample_summary = summarize_folder_files("tests/resources")
        >>> print_pandas(sample_summary)
                              file_rootpath                   filename  encoding
        filetype  subtype
            text       csv  tests/resources          video_formats.csv      None
                  markdown  tests/resources         resources_index.md      None
                  x-python  tests/resources  print_mimetype_guesses.py      None
                      yaml  tests/resources          video_formats.yml      None

    """
    raw_table = _make_raw_summary_table(iterates_file_paths=iterates_file_paths)
    if raw_table.empty:
        return _make_empty_table()
    finished_table = _split_mimetype_of_summary_table(raw_table=raw_table)
    finished_table.set_index([_COLUMN_FILETYPE, _COLUMN_SUBTYPE], inplace=True)
    finished_table.sort_index(inplace=True)
    return finished_table


def summarize_folder_files(folder_path: APath) -> DataFrame:
    """
    Summarizes the content of the *folder path*.

    Args:
        folder_path:
            Path which content is summarized.

    Returns:
        DataFrame

    Examples:
        >>> from pathsummary import summarize_folder_files
        >>> from doctestprinter import print_pandas
        >>> sample_summary = summarize_folder_files("tests/resources/images")
        >>> print_pandas(sample_summary)
                                    file_rootpath      filename  encoding
        filetype  subtype
           image      bmp  tests/resources/images   image00.bmp      None
                      bmp  tests/resources/images   image01.BMP      None
                     jpeg  tests/resources/images  image00.jpeg      None
                     jpeg  tests/resources/images   image00.jpg      None
                     jpeg  tests/resources/images  image01.JPEG      None
                     jpeg  tests/resources/images   image01.JPG      None
                      png  tests/resources/images   image00.png      None
                      png  tests/resources/images   image01.PNG      None
                     tiff  tests/resources/images   image00.tif      None
                     tiff  tests/resources/images  image00.tiff      None
                     tiff  tests/resources/images   image01.TIF      None
                     tiff  tests/resources/images  image01.TIFF      None

        >>> counts_of_equal_types = sample_summary.index.value_counts()
        >>> counts_of_equal_types.sort_index(inplace=True)
        >>> print_pandas(counts_of_equal_types, formats="{:<}#{:>}")
        ('image', 'bmp')   2
        ('image', 'jpeg')  4
        ('image', 'png')   2
        ('image', 'tiff')  4

    """
    folder_path = Path(folder_path).expanduser()

    if not folder_path.exists():
        return {}
    if not folder_path.is_dir():
        return {}

    iterates_file_paths = walk_file_paths(
        root_path=folder_path, filter_pattern=_SELECT_ALL_FILES, recursive=False
    )

    return _make_path_summary(iterates_file_paths=iterates_file_paths)


def count_type_occurrences(summary_table: DataFrame) -> DataFrame:
    """
    Counts the occurences of file- and subtypes.

    Args:
        summary_table:
            The summarized content of a path.

    Returns:
        DataFrame

    Examples:
        >>> from pathsummary import summarize_folder_files, count_type_occurrences
        >>> from doctestprinter import print_pandas
        >>> sample_summary = summarize_folder_files("tests/resources/images")
        >>> sample_counts = count_type_occurrences(sample_summary)
        >>> print_pandas(sample_counts, formats="{}#{:}{:.0%}")
                           count  ratio
        filetype  subtype
           image      bmp      2    17%
                     jpeg      4    33%
                      png      2    17%
                     tiff      4    33%

    """
    unique_counts = summary_table.index.value_counts()
    unique_counts.name = _COLUMN_UNIQUE_COUNTS

    total_count = unique_counts.sum()
    relative_counts = unique_counts / total_count
    relative_counts.name = _COLUMN_REL_COUNTS

    unique_and_relative_counts = pandas.concat([unique_counts, relative_counts], axis=1)

    multi_index = pandas.MultiIndex.from_tuples(
        unique_counts.index, names=[_COLUMN_FILETYPE, _COLUMN_SUBTYPE]
    )
    type_occurrences = DataFrame(unique_and_relative_counts, index=multi_index)
    type_occurrences.sort_index(inplace=True)
    return type_occurrences


class PathSummary:
    def __init__(self, summary_table: DataFrame):
        if not isinstance(summary_table, DataFrame):
            raise TypeError("The summary_table must be a pandas.DataFrame.")
        self._table: DataFrame = summary_table

    def __str__(self):
        file_names = self.table["filename"].to_list()
        joined_filenames = ", ".join(file_names)
        return "{}({})".format(self.__class__.__name__, joined_filenames)

    def __repr__(self):
        return str(self.table)

    @property
    def table(self) -> DataFrame:
        return self._table

    @property
    def empty(self) -> bool:
        """
        States if the path summary is empty.

        Returns:
            bool
        """
        return self.table.empty

    @property
    def filenames(self) -> List[str]:
        """
        Returns all filenames of the path.

        Returns:
            List[str]

        Examples:

            >>> from pathsummary import PathSummary
            >>> from doctestprinter import doctest_print
            >>> from pathlib import Path
            >>> test_paths = [
            ...     Path("a/path/Ariadne.txt"),
            ...     Path("a/path/Bob.txt"),
            ...     Path("a/path/Ariadne.bmp"),
            ...     Path("a/path/Bob.bmp"),
            ... ]
            >>> sample_summary = PathSummary.from_file_paths(test_paths)
            >>> doctest_print(sample_summary.filenames, max_line_width=60)
            ['Ariadne.bmp', 'Ariadne.txt', 'Bob.bmp', 'Bob.txt']
        """
        if self.empty:
            return []
        unsorted_filenames = self.table[_COLUMN_FILENAME].to_list()
        sorted_filenames = list(sorted(unsorted_filenames))
        return sorted_filenames

    @staticmethod
    def summarize_path(folder_path: APath) -> "PathSummary":
        """
        Summarizes the content of the given *folder path*.

        Args:
            folder_path:
                The folder path which content is summarized.

        Returns:
            PathSummary

        Examples:
            >>> from pathsummary import PathSummary
            >>> from doctestprinter import print_pandas
            >>> from pathlib import Path
            >>> test_path = "tests/resources/images"
            >>> sample_summary = PathSummary.summarize_path(test_path)
            >>> print_pandas(sample_summary.table)
                                        file_rootpath      filename  encoding
            filetype  subtype
               image      bmp  tests/resources/images   image00.bmp      None
                          bmp  tests/resources/images   image01.BMP      None
                         jpeg  tests/resources/images  image00.jpeg      None
                         jpeg  tests/resources/images   image00.jpg      None
                         jpeg  tests/resources/images  image01.JPEG      None
                         jpeg  tests/resources/images   image01.JPG      None
                          png  tests/resources/images   image00.png      None
                          png  tests/resources/images   image01.PNG      None
                         tiff  tests/resources/images   image00.tif      None
                         tiff  tests/resources/images  image00.tiff      None
                         tiff  tests/resources/images   image01.TIF      None
                         tiff  tests/resources/images  image01.TIFF      None

        """
        folder_path = Path(folder_path)
        if not folder_path.exists():
            raise FileExistsError("The given path doesn't exists.")
        path_summary_table = summarize_folder_files(folder_path=folder_path)
        assert isinstance(
            path_summary_table, DataFrame
        ), "The table must be a DataFrame."
        return PathSummary(summary_table=path_summary_table)

    @staticmethod
    def from_file_paths(file_paths: List[Path]) -> "PathSummary":
        """
        Creates a *path summary* based on the given file paths.

        Args:
            file_paths:
                File paths of the path summary.

        Returns:
            PathSummary

        Examples:
            >>> from pathsummary import summarize_folder_files
            >>> from doctestprinter import print_pandas
            >>> from pathlib import Path
            >>> test_file_paths = [
            ...     Path("tests/resources/images/image01.BMP"),
            ...     Path("tests/resources/images/image00.jpeg"),
            ...     Path("tests/resources/images/image00.jpg"),
            ...     Path("tests/resources/images/image01.JPEG"),
            ...     Path("tests/resources/images/image01.JPG"),
            ... ]
            >>> sample_summary = PathSummary.from_file_paths(test_file_paths)
            >>> print_pandas(sample_summary.table)
                                        file_rootpath      filename  encoding
            filetype  subtype
               image      bmp  tests/resources/images   image01.BMP      None
                         jpeg  tests/resources/images  image00.jpeg      None
                         jpeg  tests/resources/images   image00.jpg      None
                         jpeg  tests/resources/images  image01.JPEG      None
                         jpeg  tests/resources/images   image01.JPG      None

        .. doctest::

            >>> test_file_paths = [
            ...     Path("tests/resources/images/image01.BMP"),
            ... ]
            >>> sample_summary = PathSummary.from_file_paths(test_file_paths)
            >>> print_pandas(sample_summary.table)
                                        file_rootpath     filename  encoding
            filetype  subtype
               image      bmp  tests/resources/images  image01.BMP      None

        """
        path_summary_table = _make_path_summary(iterates_file_paths=file_paths)
        return PathSummary(summary_table=path_summary_table)

    def select(
        self, file_type: List[str], sub_type: Optional[List[str]] = None
    ) -> "PathSummary":
        """
        Returns a new PathSummary filtered by the *file type* and
        optional the *sub_type*.

        Args:
            file_type:
                Files based on the file type are yielded.

            sub_type:
                Optional sub type to narrow the selection down.

        Returns:
            PathSummary

        Examples:

            >>> from doctestprinter import print_pandas
            >>> from pathsummary import PathSummary
            >>> from pathlib import Path
            >>> sample_paths = [
            ...     Path("image-01.jpg"),
            ...     Path("image-02.jpg"),
            ...     Path("image-01.bmp"),
            ...     Path("textfile-01.txt"),
            ...     Path("textfile-02.csv"),
            ... ]
            >>> sample_summary = PathSummary.from_file_paths(sample_paths)
            >>> print_pandas(sample_summary.table)
                               file_rootpath         filename  encoding
            filetype  subtype
               image      bmp              .     image-01.bmp      None
                         jpeg              .     image-01.jpg      None
                         jpeg              .     image-02.jpg      None
                text      csv              .  textfile-02.csv      None
                        plain              .  textfile-01.txt      None


            The path summary can be filtered by the desired file type.

            >>> filtered_sample = sample_summary.select(FileTypes.IMAGE)
            >>> print_pandas(filtered_sample.table)
                               file_rootpath      filename  encoding
            filetype  subtype
               image      bmp              .  image-01.bmp      None
                         jpeg              .  image-01.jpg      None
                         jpeg              .  image-02.jpg      None


            And being additionally deeper filtered by the sub type.

            >>> deeper_filtered_sample = sample_summary.select(FileTypes.IMAGE, "jpeg")
            >>> print_pandas(deeper_filtered_sample.table)
                               file_rootpath      filename  encoding
            filetype  subtype
               image     jpeg              .  image-01.jpg      None
                         jpeg              .  image-02.jpg      None


            An empty result is returned, if requested types doesn't occur.

            >>> empty_sample = sample_summary.select(FileTypes.IMAGE, "tif")
            >>> print_pandas(empty_sample.table)
            Empty DataFrame
            Columns: [file_rootpath, filename, mimetype, encoding]
            Index: []
        """
        if sub_type is not None:
            selection = (file_type, sub_type)
        else:
            selection = (file_type, slice(None))

        try:
            filtered_table = self.table.loc[selection, :].copy(deep=True)
            return PathSummary(summary_table=filtered_table)
        except KeyError:
            empty_index = pandas.MultiIndex(
                levels=[[], []],
                codes=[[], []],
                names=[_COLUMN_FILETYPE, _COLUMN_SUBTYPE],
            )
            empty_table = DataFrame(index=empty_index, columns=_RAW_TABLE_COLUMNS)
            return PathSummary(summary_table=empty_table)

    def iter_by_filetype(self, file_type: str, sub_type: Optional[str] = None) -> Path:
        """
        Iterates the filepaths releated to the *file type* and optionally *sub type*.

        Args:
            file_type:
                Files based on the file type are yielded.

            sub_type:
                Optional sub type to narrow the selection down.

        Returns:
            Path

        Examples:
            >>> from pathsummary import summarize_folder_files, FileTypes
            >>> from doctestprinter import print_pandas, doctest_iter_print
            >>> from pathlib import Path
            >>> test_file_paths = [
            ...     Path("tests/resources/images/image01.BMP"),
            ...     Path("tests/resources/images/image00.jpeg"),
            ...     Path("tests/resources/images/image00.jpg"),
            ...     Path("tests/resources/images/image01.JPEG"),
            ...     Path("tests/resources/images/image01.JPG"),
            ... ]
            >>> sample_summary = PathSummary.from_file_paths(test_file_paths)
            >>> doctest_iter_print(sample_summary.iter_by_filetype(FileTypes.IMAGE))
            tests/resources/images/image01.BMP
            tests/resources/images/image00.jpeg
            tests/resources/images/image00.jpg
            tests/resources/images/image01.JPEG
            tests/resources/images/image01.JPG

            >>> doctest_iter_print(
            ...     sample_summary.iter_by_filetype(FileTypes.IMAGE, "bmp")
            ... )
            tests/resources/images/image01.BMP


            >>> test_file_paths = [Path("a/path/text.csv")]
            >>> sample_summary = PathSummary.from_file_paths(test_file_paths)
            >>> doctest_iter_print(sample_summary.iter_by_filetype("text", "csv"))
            a/path/text.csv
        """
        if sub_type is not None:
            selection = (file_type, sub_type)
        else:
            selection = file_type

        try:
            sub_table = self.table.loc[selection]
        except KeyError:
            return None

        if isinstance(sub_table, Series):
            root_path_of_file = sub_table["file_rootpath"]
            filename = sub_table["filename"]
            yield root_path_of_file.joinpath(filename)
            return None

        for index, row in sub_table.iterrows():
            root_path_of_file = row["file_rootpath"]
            filename = row["filename"]
            yield root_path_of_file.joinpath(filename)

    def count_type_occurrences(self):
        """
        Counts the occurences of file- and subtypes.

        Returns:
            DataFrame

        Examples:
            >>> from pathsummary import PathSummary
            >>> from doctestprinter import print_pandas
            >>> sample_summary = PathSummary.summarize_path("tests/resources/images")
            >>> sample_counts = sample_summary.count_type_occurrences()
            >>> print_pandas(sample_counts, formats="{}#{:}{:.0%}")
                               count  ratio
            filetype  subtype
               image      bmp      2    17%
                         jpeg      4    33%
                          png      2    17%
                         tiff      4    33%
        """
        return count_type_occurrences(self.table)


@click.command("")
@click.argument("root-path", type=click.Path(), default="./")
@click.option(
    "--count",
    "-c",
    is_flag=True,
    default=False,
    help="Prints the sum of each subtype and its ratio towards the total file count.",
)
def cli(root_path, count: bool):
    summary = PathSummary.summarize_path(folder_path=Path(root_path))
    if count:
        counts = summary.count_type_occurrences()
        output = prepare_pandas(counts)
    else:
        output_selection = [_COLUMN_FILENAME]
        output = prepare_pandas(summary.table[output_selection])

    click.echo(output)


if __name__ == "__main__":
    cli()

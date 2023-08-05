from zstandard import decompress
from mabel.errors.invalid_data_set_error import InvalidDataSetError
from mabel.errors import MissingDependencyError
from mabel.utils import paths


def zstd(stream):
    """
    Read zstandard compressed files
    """
    # zstandard should always be present
    import zstandard  # type:ignore

    with zstandard.open(stream, "r", encoding="utf8") as file:  # type:ignore
        yield from file


def lzma(stream):
    """
    Read LZMA compressed files
    """
    # lzma should always be present
    import lzma

    with lzma.open(stream, "rb") as file:  # type:ignore
        yield from file


def unzip(stream):
    """
    Read ZIP compressed files
    """
    # zipfile should always be present
    import zipfile
    import io
    from .parallel_reader import KNOWN_EXTENSIONS

    with zipfile.ZipFile(stream, "r") as zip:
        for file_name in zipfile.ZipFile.namelist(zip):
            file = zip.read(file_name)
            # get the extention of the file(s) in the ZIP and put them
            # through a secondary decompressor and parser
            ext = "." + file_name.split(".")[-1]
            print("EXT", ext)
            if ext in KNOWN_EXTENSIONS:
                decompressor, parser, file_type = KNOWN_EXTENSIONS[ext]
                print(decompressor, parser)
                for line in decompressor(io.BytesIO(file)):
                    yield parser(line)


def parquet(stream):
    """
    Read parquet formatted files
    """
    try:
        import pyarrow.parquet as pq  # type:ignore
    except ImportError:  # pragma: no cover
        raise MissingDependencyError(
            "`pyarrow` is missing, please install or include in requirements.txt"
        )
    table = pq.read_table(stream)
    for batch in table.to_batches():
        dict_batch = batch.to_pydict()
        for index in range(len(batch)):
            yield {k: v[index] for k, v in dict_batch.items()}


def lines(stream):
    """
    Default reader, assumes text format
    """
    text = stream.read().decode("utf8")  # type:ignore
    yield from text.splitlines()


def block(stream):
    yield stream.read().decode("utf8")


def csv(stream):
    import csv

    yield from csv.DictReader(stream.read().decode("utf8").splitlines())

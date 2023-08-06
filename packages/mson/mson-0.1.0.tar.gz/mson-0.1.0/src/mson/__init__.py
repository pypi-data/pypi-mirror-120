from typing import Any, BinaryIO

from .dumping import MsonEncoder
from .parsing import MsonTransformer, lark_parser

__all__ = [
    "dump",
    "dumps",
    "load",
    "loads",
]


def dump(v: Any, f: BinaryIO) -> None:
    """
    Dumps the value in MSON format into the file handle

    Parameters
    ----------
    v
        Any MSON-compatible value
    f
        File handle
    """

    f.write(dumps(v))


def dumps(v: Any) -> bytes:
    """
    Returns a value encoded in MSON format

    Parameters
    ----------
    v
        Any MSON-compatible value
    """

    encoder = MsonEncoder()
    return encoder.encode(v)


def load(f: BinaryIO) -> Any:
    """
    Loads MSON from a file handle

    Parameters
    ----------
    f
        File handle that will be read and parsed
    """

    return loads(f.read())


def loads(s: bytes) -> Any:
    """
    Loads the MSON content from the provided string

    Parameters
    ----------
    s
        MSON string to be read
    """

    tree = lark_parser.parse(s)
    return MsonTransformer().transform(tree)

import json
import re
from collections import Mapping, Sequence
from datetime import date, datetime
from decimal import Decimal
from fractions import Fraction
from typing import Any

ESCAPE_BINARY = re.compile(br'[\r\n\x00\\"]')

NoneType = None.__class__  # noqa


class MsonEncoder:
    """
    Manages the encoding into MSON

    Other Parameters
    ----------------
    _encodings
        Contains an ordered mapping between types and the name of the encoding
        function. The order is important, by example a string is a sequence so
        if you don't evaluate it in order it will encode the string erroneously
    """

    _encodings = {
        str: "string",
        bytes: "binary",
        bool: "bool",
        datetime: "datetime",
        date: "date",
        float: "float",
        int: "int",
        Fraction: "rational",
        Decimal: "decimal",
        Sequence: "list",
        Mapping: "dict",
        NoneType: "none",
    }

    def __init__(self):
        pass

    def encode(self, data: Any) -> bytes:
        """
        Encodes the provided data into bytes

        Parameters
        ----------
        data
            Any data that can be encoded into MSON
        """

        for t, name in self._encodings.items():
            if isinstance(data, t):
                return getattr(self, f"encode_{name}")(data)

        raise ValueError(f"No encoding for type {data.__class__}")

    def encode_string(self, v: str):
        """
        Lazily re-use JSON's string encoding

        Parameters
        ----------
        v
            A unicode string
        """

        return json.dumps(v, ensure_ascii=True).encode("ascii")

    def encode_binary(self, v: bytes):
        """
        Encodes a binary string. Most of the string will be passed through,
        except a few special characters that will get escaped.

        Parameters
        ----------
        v
            String to encode
        """

        return (
            b'b"'
            + ESCAPE_BINARY.sub(
                lambda m: b"\\"
                + {
                    b"\r": b"r",
                    b"\n": b"n",
                    b"\0": b"0",
                    b'"': b'"',
                    b"\\": b"\\",
                }[m.group(0)],
                v,
            )
            + b'"'
        )

    def encode_datetime(self, v: datetime):
        """
        Encodes a datetime object into the regular ISO format

        Parameters
        ----------
        v
            Date time to encode
        """

        return v.isoformat().encode("ascii")

    def encode_date(self, v: date):
        """
        Encodes a simple date object into regular ISO format

        Parameters
        ----------
        v
            Date to encode
        """

        return v.isoformat().encode("ascii")

    def encode_float(self, v: float):
        """
        Encodes a regular float into bytes

        Parameters
        ----------
        v
            Float to encode
        """

        return str(v).encode("ascii")

    def encode_int(self, v: int):
        """
        Encodes an integer into bytes

        Parameters
        ----------
        v
            Integer to encode
        """

        return f"i{v}".encode("ascii")

    def encode_rational(self, v: Fraction):
        """
        Encodes a rational (fraction) number into a string. It's just two
        integer separated by a slash.

        Parameters
        ----------
        v
            Rational number to encode
        """

        return f"r{v.numerator}/{v.denominator}".encode("ascii")

    def encode_decimal(self, v: Decimal):
        """
        Encodes a decimal number into bytes.

        Parameters
        ----------
        v
            Decimal number to encode.
        """

        return f"d{v}".encode("ascii")

    def encode_list(self, v: Sequence):
        """
        Recursively encodes all items of the list and joins them with a coma
        into a list literal.

        Parameters
        ----------
        v
            Sequence of items to be encoded
        """

        return b"[" + b",".join(self.encode(x) for x in v) + b"]"

    def encode_dict(self, v: Mapping):
        """
        Recursively encodes all items of the mapping (key and value) and joins
        them with a coma into a dictionary literal.

        Parameters
        ----------
        v
            Dictionary to encode
        """

        return (
            b"{"
            + b",".join(self.encode(k) + b":" + self.encode(v) for k, v in v.items())
            + b"}"
        )

    def encode_none(self, v: NoneType):
        """
        The encoding of None is always the same

        Parameters
        ----------
        v
            None
        """

        return b"null"

    def encode_bool(self, v: bool):
        """
        Encodes a boolean into true or false

        Parameters
        ----------
        v
            Bool to encode
        """

        if v:
            return b"true"
        else:
            return b"false"

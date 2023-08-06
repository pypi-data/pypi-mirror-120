import json
import re
from decimal import Decimal
from fractions import Fraction
from typing import Sequence

import pendulum
from lark import Lark, Token, Transformer


def lark_quote(s: str) -> str:
    return "/" + s.replace("/", "\\/") + "/"


STRING = r"\"(([^\\\"\x00-\x1f\x7f-\xff]|\\[bfnrt\"\\]|\\u[0-9a-fA-F]{4})*)\""
BINARY = r"b\"([^\"\\\0\n\r]|\\[0nr\"\\])*\""
NUMBER_FLOAT = (
    r"[+-]?([0-9]+([.][0-9]*)?([eE][+-]?[0-9]+)?|[.][0-9]+([eE][+-]?[0-9]+)?)"
)
NUMBER_INT = r"i[+-]?[0-9]+"
NUMBER_DECIMAL = r"d[+-]?([0-9]+)?(\.[0-9]+)?"
NUMBER_RATIONAL = r"r[+-]?[0-9]+(/([0-9]+))?"
DATE = r"[+-]?[0-9]{4,}-[0-9]{2}-[0-9]{2}"
DATE_TIME = r"[+-]?[0-9]{4,}-[0-9]{2}-[0-9]{2}( \d{2}(:\d{2}(:\d{2}(\.\d+)?)?)?|T\d{2}(\d{2}(\d{2}(\.\d+)?)?)?)(Z|[+-]\d{2}(:?\d{2})?)?"

UNESCAPE_BINARY = re.compile(br'\\([rn0"\\])')


GRAMMAR = f"""
    ?value: dict
          | list
          | "true"              -> true
          | "false"             -> false
          | "null"              -> null
          | string
          | binary
          | number_float
          | number_int
          | number_decimal
          | number_rational
          | date
          | date_time

    ?hashable_value: tuple
                   | "true"              -> true
                   | "false"             -> false
                   | "null"              -> null
                   | string
                   | binary
                   | number_float
                   | number_int
                   | number_decimal
                   | number_rational
                   | date
                   | date_time

    string: {lark_quote(STRING)}
    binary: {lark_quote(BINARY)}
    number_float: {lark_quote(NUMBER_FLOAT)}
    number_int: {lark_quote(NUMBER_INT)}
    number_decimal: {lark_quote(NUMBER_DECIMAL)}
    number_rational: {lark_quote(NUMBER_RATIONAL)}
    date: {lark_quote(DATE)}
    date_time: {lark_quote(DATE_TIME)}

    list : "[" [value ("," value)*] "]"
    tuple : "[" [value ("," value)*] "]"

    dict : "{{" [pair ("," pair)*] "}}"
    pair : hashable_value ":" value

    %import common.WS
    %ignore WS
"""

lark_parser = Lark(GRAMMAR, use_bytes=True, start="value")


class MsonTransformer(Transformer):
    """
    Transforms MSON tokens into Python types
    """

    dict = dict
    tuple = tuple
    pair = tuple
    list = list

    def number_float(self, v: Sequence[Token]):
        (s,) = v
        return float(s.value.decode("ascii"))

    def number_rational(self, v: Sequence[Token]):
        (s,) = v
        return Fraction(s.value.decode("ascii")[1:])

    def number_int(self, v: Sequence[Token]):
        (s,) = v
        return int(s.value.decode("ascii")[1:])

    def number_decimal(self, v: Sequence[Token]):
        (s,) = v
        return Decimal(s.value.decode("ascii")[1:])

    def string(self, v: Sequence[Token]):
        (s,) = v
        return json.loads(s.value.decode("ascii"))

    def binary(self, v: Sequence[Token]):
        (s,) = v
        data = s.value
        return UNESCAPE_BINARY.sub(
            lambda m: {
                b"r": b"\r",
                b"n": b"\n",
                b"0": b"\0",
                b'"': b'"',
                b"\\": b"\\",
            }[m.group(1)],
            data[2:-1],
        )

    def null(self, _):
        return None

    def true(self, _):
        return True

    def false(self, _):
        return False

    def date_time(self, v: Sequence[Token]):
        (s,) = v
        return pendulum.parse(s.value.decode())

    def date(self, v: Sequence[Token]):
        (s,) = v
        return pendulum.parse(s.value.decode()).date()


if __name__ == "__main__":
    text = '["foo", "bar", b"éléphant\\n\\"géant\\"", 42, 42.42, i42, {[i42, r42/27]: i2523958209358209852039866208209352}]'.encode(
        "utf-8"
    )
    tree = lark_parser.parse(text)
    transformed = MsonTransformer().transform(tree)
    print(transformed)

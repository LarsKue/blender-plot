
from typing import NamedTuple


class Color(NamedTuple):
    red: float
    green: float
    blue: float
    alpha: float = 1.0


Color.Black = Color(0.0, 0.0, 0.0)
Color.Blue = Color(0.0, 0.0, 1.0)

Color.Green = Color(0.0, 1.0, 0.0)

Color.Red = Color(1.0, 0.0, 0.0)

Color.White = Color(1.0, 1.0, 1.0)

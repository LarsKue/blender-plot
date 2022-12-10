
import blender_plot as bp

from .color import Color
from .gradient import GradientMaterial
from .solid import SolidColorMaterial
from .static import StaticMaterial

import importlib.resources as resources
import pathlib

static_materials = resources.path(package=bp, resource="materials.blend")
static_materials = pathlib.Path(str(static_materials))

blue = SolidColorMaterial(color=Color.Blue, name="Solid Blue")

green = SolidColorMaterial(color=Color.Green, name="Solid Green")

rainbow = StaticMaterial(filepath=static_materials, name="rainbow")

red = SolidColorMaterial(color=Color.Red, name="Solid Red")
red_blue = GradientMaterial(colors=[Color.Red, Color.Blue], name="Red Blue")

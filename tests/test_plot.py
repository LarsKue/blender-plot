
import blender_plot as bp
import numpy as np


def test_plot():
    plot = bp.RenderPlot()

    data = np.random.standard_normal((128, 3))
    plot.scatter(data)
    plot.save()

    plot.render()

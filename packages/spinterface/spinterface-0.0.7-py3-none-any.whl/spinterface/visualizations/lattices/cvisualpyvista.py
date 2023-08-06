# -*- coding: utf-8 -*-
r"""
Module contains implementation of pyvista visualizations for spin lattices.
"""
from pathlib import Path
from spinterface.visualizations.lattices.utilities import get_colormap
import pyvista as pv
import numpy as np
from spinterface.visualizations.lattices.ivisualizer import IVisualizer
from spinterface.inputs.lattice.ILattice import ILattice
from typing import List, Tuple, Union


class CVisualPyVista(IVisualizer):
    r"""
    Class for visualizing spin lattices with py vista library
    """

    def __init__(self, lattice: ILattice, tiplength: float = 1.0, tipradius: float = 0.35,
                 arrowscale: float = 0.7, cam: Union[List[Tuple[float, float, float]], None] = None,
                 cmap: str = 'hsv_spind') -> None:
        r"""
        Initializes the visualization

        Args:
            tiplength(float): geometry of arrow: tiplength
            tipradius(float): geometry of arrow: tipradius
            arrowscale(float): geometry of arrow: arrowscale
            camera: camera position
            cmap: string for the choice of the colormap. Defined in utilities module
        """
        super().__init__(lattice)
        self._geom = pv.Arrow(start=np.array([-arrowscale / 2.0, 0, 0]), tip_length=tiplength,
                              tip_radius=tipradius, scale=arrowscale)
        self.cam = cam
        self.cmap = get_colormap(cmap)
        self._make_plotter()

    def _make_plotter(self, offscreen: bool = False):
        r"""
        Creates the plotter. The plotter will be recreated when saving the image
        """
        self.plotter = pv.Plotter(off_screen=offscreen, lighting='three lights')
        self._configureplotter()
        self.plotter.camera_position = self.cam
        plotpoints, plotspins, plotsz = self._make_plot_points()
        self.PolyData = pv.PolyData(plotpoints)
        self.PolyData.vectors = plotspins
        self.PolyData['oop'] = plotsz
        self.Glyphs = self.PolyData.glyph(orient=True, scale=True, geom=self._geom)
        self.plotter.add_mesh(self.Glyphs, show_scalar_bar=False, cmap=self.cmap)

    def _make_plot_points(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        r"""
        We always want to norm the colormap in the interval -1, 1 even we have a lattice which spins have only SZ comp.
        in the interval e.g. (1,0.5). There is now easy way to do this with pyvista since there is no interface for nor-
        malizing. Therefore, we add an invisible point in the center of the lattice here.

        Returns:
            the points, the spins and the sz components
        """
        plotpoints = np.append(self.lattice.points, np.array([self.lattice.midpoint, self.lattice.midpoint]), axis=0)
        plotspins = np.append(self.lattice.spins, np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]), axis=0)
        plotsz = np.append(self.lattice.SZ, np.array([1.0, -1.0]))
        return plotpoints, plotspins, plotsz

    def _configureplotter(self) -> None:
        r"""
        Configures the plotter object
        """
        pv.set_plot_theme("ParaView")
        pv.rcParams['transparent_background'] = True
        self.plotter.set_background('white')

        def cam() -> None:
            print('Camera postion: ', self.plotter.camera_position)

        self.plotter.add_key_event('c', cam)

    def show(self) -> None:
        r"""
        Shows the plotter
        """
        print('Look what you have done.......')
        print('to get current cam-position press key c')
        self.plotter.show()

    def __call__(self, outpath: Path = Path.cwd() / 'spin.png') -> None:
        r"""
        Saves the image to a file

        Args:
            outpath(Path): output path for the png image created.
        """
        self._make_plotter(offscreen=True)
        self.plotter.window_size = [4000, 4000]
        self.plotter.screenshot(str(outpath.stem))


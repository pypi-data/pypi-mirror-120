import numba_geodesic_dome as ngd
import numpy as np


class GeodesicDome:
    """Class wrapper to create and interact with a Geodesic Dome"""

    def __init__(self, freq=0) -> None:
        """Creates a given geodesic dome with a given frequency.

        Args:
            freq (int, optional): The frequency of the geodesic dome. Defaults to 0.
        """
        self.vertices, self.triangles, self.adj_list = ngd.create_geodesic_dome(freq)
        pass

    def tessellate(self, freq=1) -> None:
        """Tessellates the geodesic dome a given number of times (tessellates once if no arguments provided)

        Args:
            freq (int, optional): The number of times to tessellate. Defaults to 1.
        """
        for i in range(freq):
            self.vertices, self.triangles, self.adj_list = ngd.tessellate_geodesic_dome(
                self.vertices, self.triangles
            )

        return

    def find_neighbours(self, index: np.int64, depth=1) -> np.ndarray:
        """Finds the neighbours of a given vertex on the geodesic dome to a certain depth (defaults to 1 if not provided)

        Args:
            index (np.int64): The index of the vertex to search from
            depth (int, optional): The depth of neighbours to return. Defaults to 1.

        Returns:
            np.ndarray: An array containing the indices of all the vertex's neighbours
        """
        return ngd.find_neighbours(self.vertices, self.adj_list, index, depth)

    def get_vertices(self) -> np.ndarray:
        """Getter function for vertices

        Returns:
            np.ndarray: the vertices of the geodesic dome
        """
        return self.vertices

    def get_triangles(self) -> np.ndarray:
        """Getter function for triangles

        Returns:
            np.ndarray: the triangles of the geodesic dome
        """
        return self.triangles

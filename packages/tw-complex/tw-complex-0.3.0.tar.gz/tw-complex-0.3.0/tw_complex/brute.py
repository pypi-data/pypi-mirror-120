from math import floor
from typing import List, Tuple
import numpy as np

from scipy.spatial.distance import cdist


class CDistBrute:
    def __init__(
        self,
        ally_villages: np.ndarray,
        enemy_villages: np.ndarray,
        min_radius: float,
        max_radius: float,
        _precision: float = 1,
    ) -> None:
        self.all_ally = ally_villages
        self.all_enemy = enemy_villages
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.precision = _precision

    def result(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Brute force.

        Returns
        -------
        Tuple of np.ndarray is returned:

        (below `x` is minimum of distances to every enemy village)

        `front_lst` : array with coords `x <= min_radius`

        `back_lst` : array with coords `min_radius < x < max_radius`

        NOTES
        -----
        - Step 1: Iterate over the ally_villages
        - Step 2: Return front and back villages, we do not care much about very far ones
        """

        sq_min_radius: float = self.min_radius ** 2
        sq_max_radius: float = self.max_radius ** 2
        front_lst: List[np.ndarray] = []
        back_lst: List[np.ndarray] = []

        choosen_enemy = self.all_enemy[: floor(self.all_enemy.size * self.precision)]
        np_coords: np.ndarray
        for np_coords in self.all_ally:
            C = cdist(np.array([np_coords]), choosen_enemy, "sqeuclidean")
            x: np.float64 = np.amin(C[0])

            if x <= sq_min_radius:
                front_lst.append(np_coords)
            elif x < sq_max_radius:
                back_lst.append(np_coords)

        return np.array(front_lst), np.array(back_lst)

    def triple_result(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Brute force. This is detailed version of result method.

        Returns
        -------
        Tuple of np.ndarray is returned:

        (below `x` is minimum of distances to every enemy village)

        `front_lst` : array with coords `x <= min_radius`

        `back_lst` : array with coords `min_radius < x < max_radius`

        `away_lst` : array with coords `min_radius >= max_radius`
        
        NOTES
        -----
        - Step 1: Iterate over the ally_villages
        - Step 2: Return front and back villages, we do not care much about very far ones
        """

        sq_min_radius: float = self.min_radius ** 2
        sq_max_radius: float = self.max_radius ** 2
        front_lst: List[np.ndarray] = []
        back_lst: List[np.ndarray] = []
        away_lst: List[np.ndarray] = []

        choosen_enemy = self.all_enemy[: floor(self.all_enemy.size * self.precision)]
        np_coords: np.ndarray
        for np_coords in self.all_ally:
            C = cdist(np.array([np_coords]), choosen_enemy, "sqeuclidean")
            x: np.float64 = np.amin(C[0])

            if x <= sq_min_radius:
                front_lst.append(np_coords)
            elif x < sq_max_radius:
                back_lst.append(np_coords)
            else:
                away_lst.append(np_coords)

        return np.array(front_lst), np.array(back_lst), np.array(away_lst)

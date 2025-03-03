from math import sqrt, atan2, cos, sin
import numpy as np
from numpy import deg2rad, rad2deg
from numpy.typing import NDArray
from scipy.interpolate import interp1d

from common import Ship, Vector2, MoveSet

NDArray_float = NDArray[np.float64]


def sym(ship: Ship, times: NDArray_float, delta: float = 1e-4, moveset: MoveSet = MoveSet.FREE,
        verbose: bool = False, verboselvl: int = 0) -> tuple[NDArray_float, NDArray_float]:
    """
    Calculate the ship's coordinates and thetas at the given timestamps.

    Args:
        ship: The ship object with a `move` method to update coordinates.
        times: Array of timestamps >= 0.0.
        delta: Time step for simulation.

    Returns:
        A tuple containing:
            - coords: Array of ship coordinates at the given timestamps.
            - thetas: Array of ship thetas to next_wp at the given timestamps.
    """

    # Step 1: Simulate the ship's movement over time
    simulation_times = np.arange(0, times.max() + delta, delta)  # Include the last timestamp
    coords_list = []
    thetas_list = []
    
    # Initialize the ship's state
    ship0 = ship.copy()
    current_coords = ship0.pos
    current_theta = ship0.get_theta()
    
    for t in simulation_times:
        coords_list.append(current_coords)
        thetas_list.append(current_theta)
        
        # Update the ship's state using the `move` method
        current_coords, current_theta = ship0.move_smart(
            delta,moveset=moveset, verbose=verbose, verboselvl=verboselvl
        )
    
    # Convert lists to numpy arrays
    simulation_coords = np.array(coords_list)
    simulation_thetas = np.array(thetas_list)
    
    # Step 2: Interpolate the coordinates and thetas at the given timestamps
    interp_coords_x = interp1d(simulation_times, [sc.x for sc in simulation_coords], axis=0, kind='linear', fill_value="extrapolate")
    interp_coords_z = interp1d(simulation_times, [sc.z for sc in simulation_coords], axis=0, kind='linear', fill_value="extrapolate")
    interp_thetas = interp1d(simulation_times, simulation_thetas, axis=0, kind='linear', fill_value="extrapolate")
    
    # Get the interpolated values at the specified times
    coords_x = interp_coords_x(times)
    coords_z = interp_coords_z(times)
    coords = [Vector2(x, z) for x, z in zip(coords_x, coords_z)]
    thetas = interp_thetas(times)
    
    # Step 3: Return the results with the same shape as the input times
    return coords, thetas
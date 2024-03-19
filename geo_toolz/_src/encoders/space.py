import numpy as np


def transform_360_to_180(coord: np.ndarray) -> np.ndarray:
    """
    This function converts the coordinates that are bounded from [-180, 180]
    to coordinates bounded by [0, 360].

    Args:
        coord (np.ndarray): The input array of coordinates.

    Returns:
        np.ndarray: The output array of coordinates.
    """
    return (coord + 180) % 360 - 180


def transform_180_to_360(coord: np.ndarray) -> np.ndarray:
    """
    This function converts the coordinates that are bounded from [0, 360] to coordinates bounded by [-180, 180].

    Args:
        coord (np.ndarray): The input array of coordinates.

    Returns:
        np.ndarray: The output array of coordinates.
    """
    return coord % 360


def transform_180_to_90(coord: np.ndarray) -> np.ndarray:
    """
    This function converts the coordinates that are bounded from [-180, 180]
    to coordinates bounded by [0, 360].

    Args:
        coord (np.ndarray): The input array of coordinates.

    Returns:
        np.ndarray: The output array of coordinates.
    """
    return (coord + 90) % 180 - 90


def transform_90_to_180(coord: np.ndarray) -> np.ndarray:
    """
    This function converts the coordinates that are bounded from [0, 360]
    to coordinates bounded by [-180, 180].

    Args:
        coord (np.ndarray): The input array of coordinates.

    Returns:
        np.ndarray: The output array of coordinates.
    """
    return coord % 180
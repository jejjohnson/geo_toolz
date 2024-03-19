import numpy as np
from .space import transform_360_to_180, transform_180_to_360, transform_180_to_90, transform_90_to_180


def test_transform_360_to_180():
    # Test case 1: Single coordinate within [-180, 180]
    coord1 = np.array([-90])
    expected1 = np.array([-90])
    assert np.array_equal(transform_360_to_180(coord1), expected1)

    # Test case 2: Single coordinate outside [-180, 180]
    coord2 = np.array([270])
    expected2 = np.array([-90])
    assert np.array_equal(transform_360_to_180(coord2), expected2)

    # Test case 3: Multiple coordinates within [-180, 180]
    coord3 = np.array([-90, 0, 90])
    expected3 = np.array([-90, 0, 90])
    assert np.array_equal(transform_360_to_180(coord3), expected3)

    # Test case 4: Multiple coordinates outside [-180, 180]
    coord4 = np.array([270, 360, 450])
    expected4 = np.array([-90, 0, 90])
    assert np.array_equal(transform_360_to_180(coord4), expected4)


def test_transform_180_to_360():
    # Test case 1: Single coordinate within [-180, 180]
    coord1 = np.array([-90])
    expected1 = np.array([270])
    assert np.array_equal(transform_180_to_360(coord1), expected1)

    # Test case 2: Single coordinate outside [-180, 180]
    coord2 = np.array([270])
    expected2 = np.array([270])
    assert np.array_equal(transform_180_to_360(coord2), expected2)

    # Test case 3: Multiple coordinates within [-180, 180]
    coord3 = np.array([-90, 0, 90])
    expected3 = np.array([270, 0, 90])
    assert np.array_equal(transform_180_to_360(coord3), expected3)

    # Test case 4: Multiple coordinates outside [-180, 180]
    coord4 = np.array([270, 360, 450])
    expected4 = np.array([270, 0, 90])
    assert np.array_equal(transform_180_to_360(coord4), expected4)


def test_transform_180_to_90():
    # Test case 1: Single coordinate within [-180, 180]
    coord1 = np.array([-90])
    expected1 = np.array([-90])
    assert np.array_equal(transform_180_to_90(coord1), expected1)

    # Test case 2: Single coordinate outside [-180, 180]
    coord2 = np.array([270])
    expected2 = np.array([-90])
    assert np.array_equal(transform_180_to_90(coord2), expected2)

    # Test case 3: Multiple coordinates within [-180, 180]
    coord3 = np.array([-90, 0, 90])
    expected3 = np.array([-90, 0, -90])
    assert np.array_equal(transform_180_to_90(coord3), expected3)

    # Test case 4: Multiple coordinates outside [-180, 180]
    coord4 = np.array([270, 360, 450])
    expected4 = np.array([-90, 0, -90])
    assert np.array_equal(transform_180_to_90(coord4), expected4)


def test_transform_90_to_180():
    # Test case 1: Single coordinate within [0, 360]
    coord1 = np.array([90])
    expected1 = np.array([90])
    assert np.array_equal(transform_90_to_180(coord1), expected1)

    # Test case 2: Single coordinate outside [0, 360]
    coord2 = np.array([450])
    expected2 = np.array([90])
    assert np.array_equal(transform_90_to_180(coord2), expected2)

    # Test case 3: Multiple coordinates within [0, 360]
    coord3 = np.array([90, 180, 270])
    expected3 = np.array([90, 0, 90])
    assert np.array_equal(transform_90_to_180(coord3), expected3)

    # Test case 4: Multiple coordinates outside [0, 360]
    coord4 = np.array([450, 540, 630])
    expected4 = np.array([90, 0, 90])
    assert np.array_equal(transform_90_to_180(coord4), expected4)
import numpy as np
import xarray as xr
from fillnan import fillnan_gauss_seidel

def test_fillnan_gauss_seidel():
    # Create a sample dataset with NaN values
    lon = np.arange(0, 10)
    lat = np.arange(0, 5)
    time = np.arange(0, 3)
    data = np.random.rand(len(time), len(lat), len(lon))
    data[1, 2, 3] = np.nan
    ds = xr.Dataset({"variable": (["time", "lat", "lon"], data)}, coords={"lon": lon, "lat": lat, "time": time})

    # Call the function to fill NaN values
    filled_ds = fillnan_gauss_seidel(ds, "variable")

    # Check if NaN values are filled
    assert np.isnan(filled_ds["variable"][1, 2, 3]) == False

    # Check if the shape of the dataset is preserved
    assert filled_ds["variable"].shape == (len(time), len(lat), len(lon))

    # Add more assertions to validate the correctness of the filling
    # ...

    # Add more test cases to cover different scenarios
    # ...
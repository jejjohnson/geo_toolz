import xarray as xr


def calculate_block_maxima_ts(ds: xr.DataArray, time_freq: int=365, boundary: str="trim", side: str="center")-> xr.DataArray:
    """
    Calculate block maxima time series.

    This function calculates the block maxima time series by coarsening the input dataset along the time dimension
    and taking the maximum value within each block.

    Parameters:
    - ds (xr.Dataset): The input dataset.
    - temporal_freq (int, optional): The temporal frequency for coarsening the time dimension. Default is 365.
    - boundary (str, optional): The boundary condition for coarsening. Default is "trim".
    - side (str, optional): The side of the block to align the output. Default is "center".

    Returns:
    - xr.Dataset: The block maxima time series dataset.
    """
    # coarsen array
    return ds.coarsen(time=time_freq, side=side, boundary=boundary).max()

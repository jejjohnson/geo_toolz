import xarray as xr


def where_slice(ds: xr.Dataset, variable: str, min_val: float, max_val: float, drop=True) -> xr.Dataset:

    ds = ds.where(
        (ds[variable] >= float(min_val)) & (ds[variable] <= float(max_val)),
        drop=drop
    )
        
    return ds


def where_slice_bbox(ds: xr.Dataset, bbox) -> xr.Dataset:

    x_coords = bbox.range_x
    y_coords = bbox.range_y

    ds = ds.where(
        (ds.lon.load() >= x_coords[0]) &
        (ds.lon <= x_coords[1]) &
        (ds.lat.load() >= y_coords[0]) &
        (ds.lat <= y_coords[1]),
        drop=True
    )

    return ds
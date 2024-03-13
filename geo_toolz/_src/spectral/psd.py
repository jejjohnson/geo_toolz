from typing import List, Optional
import xrft
import xarray as xr


def psd_spacetime(
    ds: xr.Dataset, variable: str, dims: List[str], **kwargs
) -> xr.Dataset:
    """
    Calculates the Power Spectral Density (PSD) with arbitrary dimensions.

    Args:
        ds (xr.Dataset): The xarray dataset with dimensions.
        variable (str): The variable for which the PSD is calculated.
        dims (List[str]): The dimensions for the PSD.
        **kwargs: Additional keyword arguments for the xrft.power_spectrum function.

    Returns:
        xr.Dataset: The xarray dataset with the new frequency dimensions.

    Example:
        >>> psd_spacetime(
            da,                 # ssh map
            "ssh",              # variable
            ["time", "lon"],    # dimensions for power spectrum
            )
    """
    name = f"{variable}_psd"

    # compute PSD signal
    psd_signal = xrft.power_spectrum(
        ds[variable],
        dim=dims,
        scaling=kwargs.get("scaling", "density"),
        detrend=kwargs.get("detrend", "linear"),
        window=kwargs.get("window", "tukey"),
        nfactor=kwargs.get("nfactor", 2),
        window_correction=kwargs.get("window_correction", True),
        true_amplitude=kwargs.get("true_amplitude", True),
        truncate=kwargs.get("truncate", True),
    )

    return psd_signal.to_dataset(name=variable)


def psd_isotropic(
    ds: xr.Dataset, variable: str,
    dims: List[str], **kwargs
) -> xr.Dataset:
    """
    Calculates the isotropic PSD with arbitrary dimensions

    Args:
        ds (xr.Dataset): The xarray dataset with dimensions.
        variable (str): The variable we wish to calculate the PSD for.
        dims (List[str]): The dimensions for the isotropic power spectrum.
        **kwargs: Additional keyword arguments for the xrft.isotropic_power_spectrum function.

    Returns:
        xr.Dataset: The xarray dataset with the new frequency dimensions.

    Example:
        >>> psd_isotropic(
            da,                 # ssh map
            "ssh",              # variable
            ["time", "lon"],    # dimensions for isotropic power spectrum
            )
    """
    name = f"{variable}_psd"

    # compute PSD signal
    psd_signal = xrft.isotropic_power_spectrum(
        ds[variable],
        dim=dims,
        scaling=kwargs.get("scaling", "density"),
        detrend=kwargs.get("detrend", "linear"),
        window=kwargs.get("window", "tukey"),
        nfactor=kwargs.get("nfactor", 2),
        window_correction=kwargs.get("window_correction", True),
        true_amplitude=kwargs.get("true_amplitude", True),
        truncate=kwargs.get("truncate", True),
    )

    original_dims = ds.dims
    psd_signal = psd_signal.to_dataset(name=variable)

    return psd_signal
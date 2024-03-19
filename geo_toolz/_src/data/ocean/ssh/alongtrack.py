import pandas as pd
import copernicusmarine
from tqdm.auto import tqdm


ALONGTRACK_NAMES_OLD = [
    "al",
    "alg",
    "c2",
    "c2n",
    "e1",
    "e1g",
    "e2",
    "en",
    "enn",
    "g2",
    "h2a",
    "h2ag",
    "h2b",
    "h2c",
    "h2",
    "j1",
    "j1g",
    "j2",
    "j2g",
    "j2n",
    "j3",
    "s3a",
    "s3b",
    "s6a",
    "tp",
    "tpn",
]


ALONGTRACK_NAMES_NEW = [
    "al",
    "c2n",
    "h2b",
    "al",
    "j3n",
    "s3a",
    "s3b",
    "s6a",
    "swon"
]


def download_alongtrack_data_old(
        satellite: str = "c2",
        time_min: str = "2017-01-01",
        time_max: str = "2017-02-01",
        output_directory: str = ".",
        **kwargs
):  
    assert time_max <= "2023-06-01" 
    assert satellite in ALONGTRACK_NAMES_OLD
    # get dataset ID
    dataset_id = f'cmems_obs-sl_glo_phy-ssh_nrt_{satellite}-l3-duacs_PT1S'
    # filter for time periods
    filters = filter_alongtrack_times(time_min=time_min, time_max=time_max)

    for filt in filters:
        copernicusmarine.get(
            dataset_id=dataset_id,
            filter=filt,
            output_directory=output_directory,
            force_download=True,
            overwrite_output_data=True,
            **kwargs
        )

def download_alongtrack_data_new(
        satellite: str = "c2",
        time_min: str = "2017-01-01",
        time_max: str = "2017-02-01",
        output_directory: str = ".",
        **kwargs
):  
    
    # get dataset ID
    dataset_id = f'cmems_obs-sl_glo_phy-ssh_nrt_{satellite}-l3-duacs_PT1S'
    # filter for time periods
    filters = filter_alongtrack_times(time_min=time_min, time_max=time_max)

    for filt in filters:
        copernicusmarine.get(
            dataset_id=dataset_id,
            filter=filt,
            output_directory=output_directory,
            force_download=True,
            overwrite_output_data=True,
            **kwargs
        )


def filter_alongtrack_times(time_min, time_max):
    return set([f"*{d.year}{d.month:02}*" for d in pd.date_range(time_min, time_max)])

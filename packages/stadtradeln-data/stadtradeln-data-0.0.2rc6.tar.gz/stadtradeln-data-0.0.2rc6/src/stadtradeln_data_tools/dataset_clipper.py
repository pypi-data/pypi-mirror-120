import pandas as pd
from typing import Tuple
from dataclasses import dataclass
from stadtradeln_data_tools.status import Status


@dataclass
class ClipResult:
    status: Status
    filepath: str


def clip_dataset(
        df: pd.DataFrame,
        latitude_lim: Tuple[float, float],
        longitude_lim: Tuple[float, float],
) -> pd.DataFrame:
    """Clips the given dataset to a desired rectangular geographic region.
    :param df: The dataset.
    :param latitude_lim: A tuple containing minimum and maximum allowed latitude values.
    :param longitude_lim: A tuple containing minimum and maximum allowed longitude values.
    :returns: The clipped dataset.
    """
    df = df[df.latitude_start.between(latitude_lim[0], latitude_lim[1])]
    df = df[df.latitude_end.between(latitude_lim[0], latitude_lim[1])]
    df = df[df.longitude_start.between(longitude_lim[0], longitude_lim[1])]
    df = df[df.longitude_end.between(longitude_lim[0], longitude_lim[1])]
    return df

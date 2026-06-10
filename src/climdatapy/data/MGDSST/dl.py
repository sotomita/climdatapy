#! /usr/bin/env python3

from datetime import datetime, timedelta
import gzip
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import io
import warnings
import logging
import requests


def get_url(time: datetime, re: bool = True) -> str:

    return (
        f"https://www.data.jma.go.jp/goos/data/pub/JMA-product/mgd_sst_glb_D/{time:%Y}/"
        f"{'re_' if re else ''}mgd_sst_glb_D{time:%Y%m%d}.txt.gz"
    )


def get_save_fpath(time: datetime, data_dir: Path, re: bool = True) -> Path:

    return data_dir / Path(
        f"MGDSST/Daily/{time:%Y}/{time:%Y%m}/{'re_' if re else ''}mgd_sst_glb_D{time:%Y%m%d}.nc"
    )


def mgdsst_download(
    start_time: datetime,
    end_time: datetime,
    data_dir: Path,
    exist_skip: bool = False,
    re: bool = True,
) -> None:

    time_list = []
    time = start_time
    while time <= end_time:
        time_list.append(time)
        time += timedelta(days=1)

    for time in time_list:

        url = get_url(time, re=re)
        save_fpath = get_save_fpath(time, data_dir, re=re)
        save_fpath.parent.mkdir(parents=True, exist_ok=True)

        r = requests.get(url, stream=True)
        r.raise_for_status()
        text: str = gzip.decompress(r.content).decode("utf-8")

        if text is None:
            warnings.warn(f'Error while downloading "{url}".')
        else:
            f = io.StringIO(text)

        text: str = gzip.decompress(r.content).decode("utf-8")

        f = io.StringIO(text)
        with f:
            df = pd.read_fwf(f, widths=[3] * 1440, nrows=720, header=None)
            arr = df.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float).copy()
            ice = (arr == 888).astype(int)
            land = (arr == 999).astype(int)
            arr[arr == 888] = np.nan
            arr[arr == 999] = np.nan
            arr *= 0.1
            lat = np.arange(89.875, -89.875 - 0.25, -0.25)
            lon = np.arange(0.125, 359.875 + 0.25, 0.25)

            ds = xr.Dataset(
                {
                    "sst": (("lat", "lon"), arr),
                    "seaice": (("lat", "lon"), ice),
                    "land": (("lat", "lon"), land),
                },
                coords={
                    "lat": lat,
                    "lon": lon,
                },
                attrs={"ORIGINAL_URL": url},
            )

            ds.to_netcdf(save_fpath)
            logging.info(f"{url} =(file conversion)=> {save_fpath}")

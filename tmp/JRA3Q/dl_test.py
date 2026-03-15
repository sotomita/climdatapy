#! /usr/bin/env python3

from datetime import datetime
from pathlib import Path

from climdatapy.data import JRA3Q

manager = JRA3Q()

start_time = datetime(2025, 1, 1)
end_time = datetime(2025, 2, 1)
download_kw = {
    "stats_type": ["all"],
    "data_kind": ["all"],
    "near_realtime": ["all"],
    "stats_type": ["all"],
    "std": [True],
    "var": ["all"],
}

data_dir = Path("./data")
log_file_path = Path("./jra3q.log")

manager.download(
    start_time,
    end_time,
    download_kw,
    data_dir,
    log_file_path,
    exist_ok=False,
)

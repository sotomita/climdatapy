#! /usr/bin/env python3

from datetime import datetime, timedelta, UTC
from pathlib import Path
from typing import Any

from ...util import Dataset
from . import dl


class MGDSST(Dataset):

    def __init__(self) -> None:
        super().__init__()

        self.min_time = datetime(1982, 1, 1)

    def get_request_key(
        self, download_kw: dict[str, list[str]], **kwargs
    ) -> list[dict[str, Any]]:

        request_key_list = []
        if "all" in download_kw["re"]:
            download_kw["re"] = ["True", "False"]

        for re in download_kw["re"]:
            request_key_list.append({"re": re})

        return request_key_list

    def get_request_time_range(
        self, start_time: datetime, end_time: datetime, request_kw: dict[str, Any]
    ) -> tuple[datetime, datetime]:

        min_start_time = self.min_time
        max_end_time = datetime.now() - timedelta(days=1)

        request_start_time = (
            start_time if min_start_time < start_time else min_start_time
        )

        if end_time < request_start_time:
            request_end_time = request_start_time
        elif end_time > max_end_time:
            request_end_time = max_end_time

        else:
            request_end_time = end_time

        return request_start_time, request_end_time

    def get_all_download_key(self) -> dict[str, list[str]]:

        return {"": [""]}

    def dl_file(
        self,
        start_time: datetime,
        end_time: datetime,
        request_kw: dict[str, Any],
        data_dir: Path,
        exist_ok: bool = False,
    ) -> None:

        re = request_kw.get("re", "True") == "True"

        dl.mgdsst_download(
            start_time,
            end_time,
            data_dir,
            exist_ok,
            re=re,
        )

    def get_newest_time(self, request_kw: dict[str, list[Any]]) -> datetime:

        re = request_kw.get("re", True)
        if re:
            return datetime.now() - timedelta(days=300)
        else:
            now_time = datetime.now(UTC).replace(tzinfo=None)
            if now_time.hour >= 10:
                newest_time = datetime.now() - timedelta(days=1)
            else:
                newest_time = datetime.now() - timedelta(days=2)

            return newest_time

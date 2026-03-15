#! /usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import datetime
import logging
from pathlib import Path
from typing import Any
from tqdm import tqdm

from .log import log_to_file


class Dataset(ABC):
    """
    気象・海洋データセットを管理する抽象クラス
    """

    @abstractmethod
    def get_request_key(
        self,
        download_kw: dict[str, list[Any]],
        **kwargs,
    ) -> list[dict[str, Any]]:

        pass

    @abstractmethod
    def dl_file(
        self,
        start_time: datetime,
        end_time: datetime,
        request_kw: dict[str, Any],
        data_dir: Path,
        exist_ok: bool = False,
    ) -> None:

        pass

    @log_to_file()
    def download(
        self,
        start_time: datetime,
        end_time: datetime,
        download_kw: dict[str, list[Any]],
        data_dir: Path,
        log_file_path: Path,
        exist_ok: bool = False,
    ) -> None:

        request_kw_list = self.get_request_key(download_kw)

        for i, request_kw in enumerate(request_kw_list):

            code = self.dl_file(start_time, end_time, request_kw, data_dir, exist_ok)
            if code is None:
                logging.info(f"[{i+1:8d}/{len(request_kw_list)}]")

    @abstractmethod
    def get_newest_time(self, request_kw: dict[str, list[Any]]) -> datetime:

        pass

    @log_to_file()
    def update(
        self,
        download_kw: dict[str, Any],
        data_dir: Path,
        log_file_path: Path,
        exist_ok: bool = False,
    ) -> None:

        request_kw_list = self.get_request_key(download_kw)
        for request_kw in request_kw_list:
            start_time = self.get_newest_time(request_kw)
            end_time = start_time
            self.dl_file(start_time, end_time, request_kw, data_dir, exist_ok)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

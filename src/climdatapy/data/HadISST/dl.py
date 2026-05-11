#! /usr/bin/env python3

from datetime import datetime
from pathlib import Path
import urllib.request
import gzip
import shutil
import logging
import warnings


def get_url() -> str:
    # HadISSTのデータ配布元URL（Met Office）
    return "https://www.metoffice.gov.uk/hadobs/hadisst/data/HadISST_sst.nc.gz"


def get_save_fpath(data_dir: Path) -> Path:
    # 保存先のファイルパス（HadISSTフォルダの中に保存）
    return data_dir / Path("HadISST/HadISST_sst.nc")


def hadisst_download(
    start_time: datetime, end_time: datetime, data_dir: Path, exist_skip: bool = False
) -> None:
    url = get_url()
    save_fpath = get_save_fpath(data_dir)

    # 保存先のフォルダが存在しない場合は作成する
    save_fpath.parent.mkdir(parents=True, exist_ok=True)

    # ダウンロードしてくる圧縮(.gz)ファイルの名前
    gz_path = save_fpath.with_suffix(".nc.gz")

    try:
        logging.info(f"Downloading HadISST from {url} ...")

        # 1. データのダウンロード
        urllib.request.urlretrieve(url, gz_path)

        # 2. .gzファイルの解凍と保存
        with gzip.open(gz_path, "rb") as f_in:
            with open(save_fpath, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # 3. 解凍が終わったら元の圧縮ファイル(.gz)はお掃除して削除
        gz_path.unlink()

        logging.info(f"{url} =(download & unzip)=> {save_fpath}")

    except Exception as e:
        warnings.warn(f'Error while downloading "{url}": {e}')

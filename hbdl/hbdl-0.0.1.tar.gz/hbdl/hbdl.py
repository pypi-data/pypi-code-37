#!/usr/bin/env python
# -*-coding: utf-8-*-

import subprocess
from dataclasses import dataclass
from hashlib import sha1
from io import DEFAULT_BUFFER_SIZE
from itertools import chain
from os import PathLike
from pathlib import Path
from typing import Callable, Dict, Iterable, List
from urllib.parse import parse_qs, urlparse

import click
import requests


def _flatten(func):
    def inner(*args, **kwargs):
        return list(chain(*func(*args, **kwargs)))

    return inner


def _shell_out(cmd, **kwargs) -> str:
    output = subprocess.check_output(cmd, shell=True, **kwargs)
    return output.decode("utf-8")


@dataclass
class Downloadable:
    fname: str
    uri: str
    sha1_hash: str

    @classmethod
    def from_dict(cls, product_data: Dict) -> Iterable:
        downloads = product_data.get("downloads", [])
        for download in downloads:
            download_structs = download.get("download_struct", [])
            for struct in download_structs:
                uri = struct.get("url", {}).get("web", "")
                if uri:
                    (_, _, file_path, _, _, _) = urlparse(uri)
                    fname = file_path[1:] if file_path.startswith("/") else file_path
                    yield Downloadable(fname=fname, uri=uri, sha1_hash=struct.get("sha1", ""))

    def download(self, to_dir: PathLike, downloader: str, echo: Callable) -> Path:
        assert downloader in ("wget", "curl", "python"), "The downloader must be one of (wget, curl, python)"
        (_, netloc, file_path, _, _, _) = urlparse(self.uri)
        assert netloc == "dl.humble.com", "Must be a humble bundle uri"
        dest_file = Path(to_dir) / (file_path[1:] if file_path.startswith("/") else file_path)
        download_op = _download_op(self, downloader, Path(to_dir))
        output = download_op()
        echo(output)
        return dest_file


def _download_op(downloadable: Downloadable, downloader: str, to_dir: Path) -> Callable:
    assert to_dir.is_dir(), f"The destination is not a dir: {to_dir}"
    assert downloader in ("wget", "curl", "python"), "The downloader must be one of (wget, curl, python)"

    def verify_sha1(downloaded: Path, sha1_hash: str):
        assert downloaded.is_file(), f"The downloaded should be a file: {downloaded}"
        if sha1_hash:
            file_hash = sha1()
            with downloaded.open(mode="rb") as fd:
                for chunk in iter(lambda: fd.read(DEFAULT_BUFFER_SIZE), b""):
                    file_hash.update(chunk)
            assert (
                file_hash.hexdigest() == sha1_hash
            ), f"The hash for downloaded not equal to the expected: {file_hash.hexdigest()} != {sha1_hash}"

    dest_file = to_dir / downloadable.fname

    def wget_download() -> str:
        cmd = f"wget -c '{downloadable.uri}' -O {dest_file}"
        output = _shell_out(cmd, stderr=True)
        verify_sha1(dest_file, downloadable.sha1_hash)
        return output

    def curl_download():
        cmd = f"curl '{downloadable.uri}' --output {dest_file}"
        output = _shell_out(cmd, stderr=True)
        verify_sha1(dest_file, downloadable.sha1_hash)
        return output

    def python_download():
        with requests.Session() as session:
            resp = session.get(downloadable.uri, stream=True)
            with dest_file.open(mode="wb") as fd:
                for chunk in resp.iter_content(chunk_size=DEFAULT_BUFFER_SIZE):
                    fd.write(chunk)
        return str(dest_file)

    if downloader == "wget":
        return wget_download
    elif downloader == "curl":
        return curl_download
    else:
        return python_download


def uri_to_purchase_key(uri: str) -> str:
    (_, netloc, file_path, _, query, _) = urlparse(uri)
    assert "humblebundle.com" in netloc, "Must be a humble bundle uri"
    queries = parse_qs(query)
    assert "key" in queries, "No dict key 'key' in the url queries"
    key, *_ = queries["key"]
    return key


@_flatten
def purchased_downloadables(purchase_key: str) -> List[Iterable[Downloadable]]:
    api_uri = f"https://www.humblebundle.com/api/v1/order/{purchase_key}?wallet_data=true&all_tpkds=true"
    purchase_data = requests.get(api_uri).json()
    products = purchase_data.get("subproducts", [])
    return [Downloadable.from_dict(product) for product in products]


@click.command()
@click.argument("uri", type=str)
@click.option("--dest-dir", type=click.Path(resolve_path=True), default=".")
@click.option("--downloader", type=click.Choice(["wget", "curl", "python"]), default="wget")
def download(uri: str, dest_dir: PathLike, downloader: str):
    key = uri_to_purchase_key(uri)
    downloables: List[Downloadable] = purchased_downloadables(key)
    for downloable in downloables:
        downloable.download(dest_dir, downloader, click.echo)

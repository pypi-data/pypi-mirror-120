# -*- coding: utf-8 -*-
# Copyright 2021, SERTIT-ICube - France, https://sertit.unistra.fr/
# This file is part of eoreader project
#     https://github.com/sertit/eoreader
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Utils: mostly getting directories relative to the project """
import logging
import os
import platform
from pathlib import Path
from typing import Union

import xarray as xr
from cloudpathlib import AnyPath, CloudPath
from distributed import Lock
from rasterio.enums import Resampling
from sertit import rasters

from eoreader.env_vars import USE_DASK

EOREADER_NAME = "eoreader"
DATETIME_FMT = "%Y%m%dT%H%M%S"
LOGGER = logging.getLogger(EOREADER_NAME)


def get_src_dir() -> Union[CloudPath, Path]:
    """
    Get src directory.

    Returns:
        str: Root directory
    """
    return AnyPath(__file__).parent


def get_root_dir() -> Union[CloudPath, Path]:
    """
    Get root directory.

    Returns:
        str: Root directory
    """
    return get_src_dir().parent


def get_data_dir() -> Union[CloudPath, Path]:
    """
    Get data directory.

    Returns:
        str: Data directory
    """
    data_dir = get_src_dir().joinpath("data")
    if not data_dir.is_dir() or not list(data_dir.iterdir()):
        data_dir = None
        # Last resort try
        if platform.system() == "Linux":
            data_dirs = AnyPath("/usr", "local", "lib").glob("**/eoreader/data")
        else:
            data_dirs = AnyPath("/").glob("**/eoreader/data")

        # Look for non empty directories
        for ddir in data_dirs:
            if len(os.listdir(ddir)) > 0:
                data_dir = ddir
                break

        if not data_dir:
            raise FileNotFoundError("Impossible to find the data directory.")

    return data_dir


def get_split_name(name: str) -> list:
    """
    Get split name (with _). Removes empty index.

    Args:
        name (str): Name to split

    Returns:
        list: Split name
    """
    return [x for x in name.split("_") if x]


# flake8: noqa
def use_dask():
    """Use Dask or not"""
    # Check environment variable
    use_dask = os.getenv(USE_DASK, "0").lower() in ("1", "true")

    # Check installed libs
    if use_dask:
        try:
            import dask
            import distributed
        except ImportError:
            use_dask = False

    return use_dask


def read(
    path: Union[str, CloudPath, Path],
    resolution: Union[tuple, list, float] = None,
    size: Union[tuple, list] = None,
    resampling: Resampling = Resampling.nearest,
    masked: bool = True,
    indexes: Union[int, list] = None,
    **kwargs,
) -> xr.DataArray:
    """
    Overload of `sertit.rasters.read()` managing  DASK in EOReader's way.

    ```python
    >>> raster_path = "path\\to\\raster.tif"
    >>> xds1 = read(raster_path)
    >>> # or
    >>> with rasterio.open(raster_path) as dst:
    >>>    xds2 = read(dst)
    >>> xds1 == xds2
    True
    ```

    Args:
        path (Union[str, CloudPath, Path]): Path to the raster
        resolution (Union[tuple, list, float]): Resolution of the wanted band, in dataset resolution unit (X, Y)
        size (Union[tuple, list]): Size of the array (width, height). Not used if resolution is provided.
        resampling (Resampling): Resampling method
        masked (bool): Get a masked array
        indexes (Union[int, list]): Indexes to load. Load the whole array if None.
        **kwargs: Optional keyword arguments to pass into rioxarray.open_rasterio().
    Returns:
        Union[XDS_TYPE]: Masked xarray corresponding to the raster data and its meta data

    """
    return rasters.read(
        path,
        resolution=resolution,
        size=size,
        resampling=resampling,
        masked=masked,
        indexes=indexes,
        chunks=True,
    )


def write(xds: xr.DataArray, path: Union[str, CloudPath, Path], **kwargs) -> None:
    """
    Overload of `sertit.rasters.write()` managing  DASK in EOReader's way.

    ```python
    >>> raster_path = "path\\to\\raster.tif"
    >>> raster_out = "path\\to\\out.tif"

    >>> # Read raster
    >>> xds = read(raster_path)

    >>> # Rewrite it
    >>> write(xds, raster_out)
    ```

    Args:
        xds (xr.DataArray): Path to the raster or a rasterio dataset or a xarray
        path (Union[str, CloudPath, Path]): Path where to save it (directories should be existing)
        **kwargs: Overloading metadata, ie `nodata=255` or `dtype=np.uint8`
    """
    if use_dask():
        from distributed import get_client

        lock = Lock("rio", client=get_client())
    else:
        lock = None

    return rasters.write(xds=xds, path=path, lock=lock, **kwargs)

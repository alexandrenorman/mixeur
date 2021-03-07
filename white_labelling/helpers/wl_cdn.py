import json
from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any

import jsonmerge
import sentry_sdk
import yaml
from django.core.cache import caches

if TYPE_CHECKING:
    from white_labelling.models import WhiteLabelling


def __read_json__(path: Path) -> dict:
    """
    Return json values as dict from a file
    May return empty dict if file was not found or empty
    Or error message if json error occurs
    """
    try:
        with path.open() as f:
            content = f.read()
            if not content.strip():
                return {}

            data = json.loads(content)

    except FileNotFoundError:
        return {}

    except Exception as e:
        sentry_sdk.capture_exception(e)
        return {"error": str(e)}

    return data


def __read_yaml__(path: Path) -> dict:
    """
    Return yaml values as dict from a file
    May return error message if yaml error occurs
    """
    with path.open() as f:
        try:
            return yaml.load(f, Loader=yaml.FullLoader)
        except yaml.scanner.ScannerError as e:
            sentry_sdk.capture_exception(e)
            return {"error": str(e)}


def __aggregate_data_files__(path: str) -> dict:
    """
    agregate all json and yaml files from a given path

    structure is :
    {
        "filename1": {...},
        "filename2": {...},
    }
    """
    data = {}

    for filepath in Path(path).glob("*.json"):
        name = filepath.stem
        data[name] = __read_json__(filepath)

    for filepath in Path(path).glob("*.y*ml"):
        name = filepath.stem
        # json has precedence over yaml (skip if same filename already processed)
        if name not in data:
            data[name] = __read_yaml__(filepath)

    return data


def __get_data__(wl: "WhiteLabelling") -> dict:
    """
    Return json/yaml data merged with ones from default's cdn date
    """
    default_json = __aggregate_data_files__(path=wl.cdn_default_directory_path)
    wl_json = __aggregate_data_files__(path=wl.cdn_directory_path)

    return jsonmerge.merge(default_json, wl_json)


def read_data(wl: "WhiteLabelling", no_cache: bool = False) -> dict:
    """
    Get data of json and yaml files from wl.cdn_directory_path
    If file is not correctly formated, add error message as properties
    The result is cached for 10 minutes
    """
    if no_cache:
        return __get_data__(wl)

    cache = caches["wl_cdn_data"]
    return cache.get_or_set(wl.id, partial(__get_data__, wl), 10 * 60)


def get_data(wl: "WhiteLabelling", path: str = None, no_cache: bool = True) -> Any:
    """
    Get a specific data for given path, return None if not found
    ex: get_data(wl, "filename.my_value")
    """
    data = read_data(wl, no_cache=no_cache)

    if not path:
        return data

    keys = path.split(".")
    for key in keys:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def get_text(
    wl: "WhiteLabelling",
    path: str,
    params: dict = {},
    fallback: str = None,
    no_cache: bool = False,
) -> str:
    """
    Get a specific string data for given path. return given fallback (or empty) string if not found.
    The result can be formatted using given params dict
    ex: filename.json:
    {
        text: '{count} sheep(s)'
    }
    get_text(wl, 'filename.text', {'count': 12})
    """
    data = get_data(wl, path=path, no_cache=no_cache) or fallback
    if not data:
        return ""

    if not isinstance(data, str):
        data = str(data)

    # defaultdict ensure format not failing if param is missing
    # (default to str() which is empty string)
    params = defaultdict(str, params)
    return data.format_map(params)


def read_file(wl: "WhiteLabelling", filename: str, base_path: str = None) -> str:
    """
    Get string content of a file from wl.cdn_directory_path
    """
    path = Path(base_path or wl.cdn_directory_path, filename)
    try:
        with path.open() as f:
            return f.read()
    except FileNotFoundError:
        return ""


def header(wl: "WhiteLabelling") -> str:
    return read_file(wl, "header.html")


def footer(wl: "WhiteLabelling") -> str:
    return read_file(wl, "footer.html")


def style(wl: "WhiteLabelling") -> str:
    return read_file(wl, "style.css")

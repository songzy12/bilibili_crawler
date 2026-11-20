import os
import json
from datetime import datetime

DEFAULT_OUTPUT_DIR = "output"
URLS_FILENAME = "picture_urls.json"
PENDING_FILENAME = "pending_dynamic_ids.json"


def get_metadata_filepath(mid, output_dir=DEFAULT_OUTPUT_DIR):
    return os.path.join(output_dir, "dynamic", str(mid), URLS_FILENAME)


def load_metadata(mid, output_dir=DEFAULT_OUTPUT_DIR):
    urls_filepath = get_metadata_filepath(mid, output_dir)
    if not os.path.exists(urls_filepath):
        return {}

    with open(urls_filepath, encoding="utf-8") as f:
        return json.loads(f.read())


def dump_metadata(mid, picture_urls, output_dir=DEFAULT_OUTPUT_DIR):
    urls_filepath = get_metadata_filepath(mid, output_dir)
    make_parent_dirs_if_not_exist(urls_filepath)
    with open(urls_filepath, mode="w", encoding="utf-8") as f:
        json.dump(picture_urls, f, ensure_ascii=False, indent=4)


def load_pending_ids(mid, output_dir=DEFAULT_OUTPUT_DIR):
    filepath = os.path.join(output_dir, "dynamic", str(mid), PENDING_FILENAME)
    if not os.path.exists(filepath):
        return set()

    with open(filepath, encoding="utf-8") as f:
        pending_ids = json.load(f)
    if not isinstance(pending_ids, list) or not all(isinstance(item, str) for item in pending_ids):
        raise ValueError(f"Invalid pending dynamic IDs in {filepath}")
    return set(pending_ids)


def dump_pending_ids(mid, pending_ids, output_dir=DEFAULT_OUTPUT_DIR):
    filepath = os.path.join(output_dir, "dynamic", str(mid), PENDING_FILENAME)
    make_parent_dirs_if_not_exist(filepath)
    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(sorted(pending_ids), f, ensure_ascii=False, indent=4)


def build_picture_filepath(mid, url, pub_ts, index, output_dir=DEFAULT_OUTPUT_DIR):
    pub_dt = datetime.fromtimestamp(int(pub_ts))
    picture_name = os.path.basename(url)
    return os.path.join(
        output_dir,
        "dynamic",
        str(mid),
        pub_dt.strftime("%Y/%m/%d_%H%M%S"),
        f"{index}_{picture_name}",
    )


def dump_picture(picture_content, filepath):
    make_parent_dirs_if_not_exist(filepath)
    with open(filepath, "wb") as f:
        f.write(picture_content)


def make_parent_dirs_if_not_exist(filepath):
    parent_dir = os.path.dirname(filepath)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

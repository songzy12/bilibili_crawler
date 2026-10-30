import os
import json
from datetime import datetime

OUTPUT_ROOT_DIR = "output/dynamic"
URLS_FILENAME = "picture_urls.json"


def get_metadata_filepath(mid):
    return os.path.join(OUTPUT_ROOT_DIR, str(mid), URLS_FILENAME)


def load_metadata(mid):
    urls_filepath = get_metadata_filepath(mid)
    if not os.path.exists(urls_filepath):
        return {}

    with open(urls_filepath, encoding="utf-8") as f:
        return json.loads(f.read())


def dump_metadata(mid, picture_urls):
    urls_filepath = get_metadata_filepath(mid)
    make_parent_dirs_if_not_exist(urls_filepath)
    with open(urls_filepath, mode="w", encoding="utf-8") as f:
        json.dump(picture_urls, f, ensure_ascii=False, indent=4)


def build_picture_filepath(mid, url, pub_ts, index):
    pub_dt = datetime.fromtimestamp(int(pub_ts))
    picture_name = os.path.basename(url)
    return os.path.join(
        OUTPUT_ROOT_DIR,
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

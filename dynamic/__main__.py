import argparse
import os
import time

from . import crawler_util
from . import config
from . import dynamic_util
from . import storage_util


parser = argparse.ArgumentParser()
parser.add_argument("--force_update_all", help="Whether to force update all picture urls.")
args = parser.parse_args()


def update_metadata(metadata_dict, mid, cookie, force_update_all):
    dynamic_api_url = dynamic_util.build_dynamic_api_url(mid)
    while dynamic_api_url != "":
        api_resp = crawler_util.fetch_dynamic_api(dynamic_api_url, cookie)
        time.sleep(3)

        cur_metadata_dict = dynamic_util.parse_metadata(api_resp)
        if not has_new_metadata(metadata_dict, cur_metadata_dict) and not force_update_all:
            print(f"no new metadata in the current batch, shortcutting...")
            break
        metadata_dict.update(cur_metadata_dict)

        dynamic_api_url = dynamic_util.build_next_dynamic_api_url(mid, api_resp)

    return metadata_dict


def has_new_metadata(metadata_dict, cur_metadata_dict):
    for key in cur_metadata_dict:
        if key not in metadata_dict:
            return True
    return False


def download_picture(picture_url, pub_ts, index, cookie):
    filepath = storage_util.build_picture_filepath(picture_url, pub_ts, index)
    if os.path.exists(filepath):
        print(f"skipped: {picture_url} {filepath}")
        return

    picture_content = crawler_util.fetch_picture(picture_url, cookie)
    time.sleep(3)

    storage_util.dump_picture(picture_content, filepath)


def download_pictures(metadata_dict, cookie):
    for item in metadata_dict.values():
        pub_ts = item["upload_timestamp"]
        for index, picture_url in enumerate(item["pictures"]):
            download_picture(picture_url, pub_ts, index, cookie)


if __name__ == "__main__":
    metadata_dict = storage_util.load_metadata()    
    update_metadata(metadata_dict, config.MID, config.COOKIE, args.force_update_all)
    storage_util.dump_metadata(metadata_dict)

    download_pictures(metadata_dict, config.COOKIE)

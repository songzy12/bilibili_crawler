import argparse
import os
import time

from . import crawler_util
from . import dynamic_util
from . import storage_util


def parse_user_ids(user_ids_file):
    user_ids = []
    with open(user_ids_file, encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            user_id, separator, comment = line.partition("#")
            user_id = user_id.strip()
            if not user_id:
                continue
            if not user_id.isascii() or not user_id.isdecimal():
                raise ValueError(
                    f"Invalid user ID in {user_ids_file}:{line_number}: "
                    "expected digits before an optional # comment"
                )
            user_ids.append((int(user_id), comment.strip() if separator else ""))

    if not user_ids:
        raise ValueError(f"No user IDs found in {user_ids_file}")
    return user_ids


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


def download_picture(mid, picture_url, pub_ts, index, cookie):
    filepath = storage_util.build_picture_filepath(mid, picture_url, pub_ts, index)
    if os.path.exists(filepath):
        print(f"skipped: {picture_url} {filepath}")
        return

    picture_content = crawler_util.fetch_picture(picture_url, cookie)
    time.sleep(3)

    storage_util.dump_picture(picture_content, filepath)


def download_pictures(mid, metadata_dict, cookie):
    for item in metadata_dict.values():
        pub_ts = item["upload_timestamp"]
        for index, picture_url in enumerate(item["pictures"]):
            download_picture(mid, picture_url, pub_ts, index, cookie)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cookie-file",
        required=True,
        help="Path to a file containing the Bilibili Cookie",
    )
    parser.add_argument(
        "--user-ids-file",
        required=True,
        help="Path to a file with one user ID per line; # starts an optional comment",
    )
    parser.add_argument(
        "--force-update-all",
        "--force_update_all",
        action="store_true",
        help="Whether to force update all picture URLs",
    )
    args = parser.parse_args()

    with open(args.cookie_file, encoding="utf-8") as cookie_file:
        cookie = cookie_file.read().strip()
    if not cookie:
        raise ValueError(f"Cookie file is empty: {args.cookie_file}")

    for mid, user_name in parse_user_ids(args.user_ids_file):
        label = f" ({user_name})" if user_name else ""
        print(f"Processing user {mid}{label}")

        metadata_dict = storage_util.load_metadata(mid)
        update_metadata(metadata_dict, mid, cookie, args.force_update_all)
        storage_util.dump_metadata(mid, metadata_dict)
        download_pictures(mid, metadata_dict, cookie)


if __name__ == "__main__":
    main()

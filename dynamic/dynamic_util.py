import sys

from . import constant


def build_dynamic_api_url(mid, offset=""):
    if offset:
        return f"{constant.DYNAMIC_API_ROOT}?host_mid={mid}&offset={offset}"
    return f"{constant.DYNAMIC_API_ROOT}?host_mid={mid}"


def has_more(resp):
    return resp["data"]["has_more"]


def build_next_dynamic_api_url(mid, resp):
    if not has_more(resp):
        return ""
    return build_dynamic_api_url(mid, resp["data"]["offset"])


def parse_metadata(resp):
    metadata = {}
    skipped_ids = set()

    for item in resp["data"]["items"]:
        if item["type"] != "DYNAMIC_TYPE_DRAW":
            continue

        id_str = item["id_str"]
        module_dynamic = item["modules"]["module_dynamic"]
        major = module_dynamic["major"]
        if major is None:
            print(f"Warning: dynamic {id_str} has no image details; will retry", file=sys.stderr)
            skipped_ids.add(id_str)
            continue

        pub_ts = item["modules"]["module_author"]["pub_ts"]
        # TODO: no description in the api resp now (as of Oct 2025).
        # text = module_dynamic["desc"]["text"]
        draw = major["draw"]

        metadata[id_str] = {
            "t_url": "https://t.bilibili.com/" + id_str,
            "doc_id": draw["id"],
            "upload_timestamp": pub_ts,
            # "description": text,
            "pictures": [item["src"] for item in draw["items"]],
        }

    return metadata, skipped_ids

import json
from base64 import b64encode
from copy import deepcopy


def encode_content(content):
    return b64encode(json.dumps(content, sort_keys=True, indent=0).encode()).decode()


def deepmerge(x, y):
    overlapping_keys = x.keys() & y.keys()
    for k in overlapping_keys:
        deepmerge(x[k], y[k])
    for k in y.keys() - overlapping_keys:
        x[k] = deepcopy(y[k])
    return x


def chunk_list(lst, n):
    return [lst[i : i + n] for i in range(0, len(lst), n)]

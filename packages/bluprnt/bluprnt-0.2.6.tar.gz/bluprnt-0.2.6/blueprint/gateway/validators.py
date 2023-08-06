from re import match


def valid_id(id_):
    return (
        isinstance(id_, str)
        and 1 <= len(id_) <= 40
        and "/" not in id_
        and id_ not in [".", ".."]
        and not match("__.*__", id_)
    )


def valid_name(name):
    return isinstance(name, str) and 1 <= len(name) <= 50


def valid_repo(repo):
    return isinstance(repo, str) and all(map(valid_id, repo.split("-")))


def valid_asset(asset):
    if isinstance(asset, str):
        parts = list(filter(None, asset.split("/")))
        return len(parts) >= 2 and all(map(valid_id, parts))
    return False


def valid_chid(chid):
    return (
        isinstance(chid, str)
        and 1 <= len(chid) <= 100
        and match("[a-zA-Z0-9-]+$", chid)
    )


def valid_change_ref(ref):
    if isinstance(ref, str):
        parts = ref.split("/")
        return (
            len(parts) == 4
            and parts[0] == "change"
            and valid_id(parts[1])
            and valid_id(parts[2])
            and valid_chid(parts[3])
        )
    return False


def valid_plan_ref(ref):
    if isinstance(ref, str):
        parts = ref.split("/")
        return (
            len(parts) == 7
            and parts[0] == "prov"
            and parts[1] == "plan"
            and valid_id(parts[2])
            and valid_change_ref("/".join(parts[3:]))
        )
    return False


def valid_apply_ref(ref):
    if isinstance(ref, str):
        parts = ref.split("/")
        return (
            len(parts) == 3
            and parts[0] == "prov"
            and parts[1] == "apply"
            and valid_id(parts[2])
        )
    return False


def valid_configuration_changes(changes):
    if not isinstance(changes, list):
        return False
    for change in changes:
        if not isinstance(change, dict):
            return False
        if "address" not in change or "body" not in change:
            return False
        body = change["body"]
        if isinstance(body, dict) and "provisioner" in body.keys():
            return False
    return True

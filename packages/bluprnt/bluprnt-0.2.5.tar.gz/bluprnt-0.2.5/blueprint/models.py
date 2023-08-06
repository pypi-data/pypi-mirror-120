class AssetReference:
    def __init__(self, *paths):
        self.path = "/".join(paths)
        path_parts = self.path.split("/")
        self.id = path_parts[-1]
        self.type = path_parts[-2]
        if len(path_parts) > 2:
            self.parent = AssetReference("/".join(path_parts[:-2]))
        else:
            self.parent = None


class DBEvent:
    def __init__(self, event):
        value = event["value"] or event["oldValue"]
        fields = value.get("fields")
        self.asset = AssetReference(self._trim_document_path(value["name"]))
        self.data = self._raise_values(fields) if fields else None

    def _trim_document_path(self, path):
        return "/".join(path.split("/")[5:])

    def _raise_value(self, value_obj):
        value_type = next(iter(value_obj))
        if value_type == "mapValue":
            value = self._raise_values(value_obj[value_type])
        elif value_type == "arrayValue":
            value = [self._raise_value(v) for v in value_obj[value_type]["values"]]
        elif value_type == "referenceValue":
            value = AssetReference(self._trim_document_path(value_obj[value_type]))
        else:
            value = value_obj[value_type]
        return value

    def _raise_values(self, fields):
        values = {}
        for key in fields:
            values[key] = self._raise_value(fields[key])
        return values


class ChangeRef:
    def __init__(self, sid: str, uid: str, chid: str):
        self.sid = sid
        self.uid = uid
        self.chid = chid
        self.name = "change/{}/{}/{}".format(self.sid, self.uid, self.chid)

    @staticmethod
    def parse(branch: str):
        parts = branch.split("/")
        return ChangeRef(*parts[1:])


class PlanRef:
    def __init__(self, sid: str, change_ref: ChangeRef):
        self.sid = sid
        self.change_ref = change_ref
        self.name = "prov/plan/{}/{}".format(self.sid, self.change_ref.name)

    @staticmethod
    def parse(branch: str):
        parts = branch.split("/")
        sid = parts[2]
        change_ref = ChangeRef(*parts[4:])
        return PlanRef(sid, change_ref)


class ApplyRef:
    def __init__(self, sid: str):
        self.sid = sid
        self.name = "prov/apply/{}".format(self.sid)

    @staticmethod
    def parse(branch: str):
        parts = branch.split("/")
        return ApplyRef(*parts[2:])


class Repo:
    def __init__(self, configuration: AssetReference):
        self.cid = configuration.id
        self.wid = configuration.parent.id
        self.name = f"{self.wid}-{self.cid}"


def parse_branch(branch: str):
    if branch.startswith("change"):
        return ChangeRef.parse(branch)
    if branch.startswith("prov/apply"):
        return ApplyRef.parse(branch)
    if branch.startswith("prov/plan"):
        return PlanRef.parse(branch)
    return None

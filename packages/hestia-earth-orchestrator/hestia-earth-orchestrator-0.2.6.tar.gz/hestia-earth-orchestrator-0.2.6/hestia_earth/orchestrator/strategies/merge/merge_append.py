from hestia_earth.orchestrator.utils import _non_empty_list, update_node_version


def merge(source: dict, dest, version: str, *args):
    source = source if source is not None else []
    nodes = _non_empty_list(dest if isinstance(dest, list) else [dest])
    source.extend([update_node_version(version, n) for n in nodes])
    return source

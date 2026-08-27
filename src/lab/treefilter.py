"""Filter a list of paths against allow and deny glob patterns."""

from lab import pathspec


def filter_paths(paths, allow, deny):
    """Return ``paths`` in order, keeping each path that matches an allow
    pattern and no deny pattern.

    An empty ``allow`` list keeps everything. A matching deny pattern always
    drops the path, even when an allow pattern also matches.
    """
    result = []
    for path in paths:
        if deny and any(pathspec.match(p, path) for p in deny):
            continue
        if not allow or any(pathspec.match(p, path) for p in allow):
            result.append(path)
    return result

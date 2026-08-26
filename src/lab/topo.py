class CycleError(ValueError):
    """Raised when the dependency graph contains a cycle."""


def topo_sort(deps):
    """Return a deterministic topological ordering of ``deps``.

    ``deps`` maps each node name to the list of nodes it depends on.
    Nodes that appear only as a dependency (never as a key) are
    included and treated as having no dependencies. Where more than one
    node could be emitted, the lexicographically smallest is chosen
    first (Kahn's algorithm with a sorted frontier). A cycle raises
    :class:`CycleError` whose message contains one concrete cycle
    rendered as ``"a -> b -> a"``.
    """
    import heapq

    dependents = {}
    for name in deps:
        dependents.setdefault(name, set())
        for held in {d for d in deps[name]}:
            dependents.setdefault(held, set())
            dependents[held].add(name)

    indegree = {name: 0 for name in dependents}
    for name in deps:
        for held in {d for d in deps[name]}:
            indegree[name] += 1

    frontier = [name for name, degree in indegree.items() if degree == 0]
    heapq.heapify(frontier)

    unsorted = set(indegree)
    sorted_names = []
    while frontier:
        name = heapq.heappop(frontier)
        unsorted.remove(name)
        sorted_names.append(name)
        for dependent in dependents[name]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(frontier, dependent)

    if unsorted:
        cycle = _find_cycle(indegree, deps, unsorted)
        raise CycleError("dependency cycle detected: " + " -> ".join(cycle))

    return sorted_names


def _find_cycle(indegree, deps, unsorted):
    """Return one concrete cycle as a list, starting from its head."""
    start = min(unsorted)
    stack = [(start, [start])]
    while stack:
        node, path = stack.pop()
        for held in {d for d in deps.get(node, ())}:
            if held in path:
                cut = path[path.index(held):] + [held]
                return cut
            if held in unsorted:
                stack.append((held, path + [held]))
    return [start]

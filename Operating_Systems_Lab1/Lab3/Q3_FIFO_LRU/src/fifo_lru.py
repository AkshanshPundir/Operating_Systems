


def validate(reference, frames):
    """The reference string must not be empty and at least one frame is needed."""
    if not reference:
        raise ValueError("Reference string cannot be empty")
    if frames <= 0:
        raise ValueError("Frame count must be positive")


def fifo(reference, capacity):
    """First-in first-out replacement. Returns (hits, faults, trace)."""
    validate(reference, capacity)

    frames = []
    pointer = 0
    hits = 0
    faults = 0
    trace = []

    for page in reference:
        if page in frames:
            hits += 1
            status = "H"
        else:
            faults += 1
            status = "F"
            if len(frames) < capacity:
                frames.append(page)
            else:
                frames[pointer] = page
                pointer = (pointer + 1) % capacity
        trace.append((page, frames[:], status))

    return hits, faults, trace


def lru(reference, capacity):
    """Least-recently-used replacement. Returns (hits, faults, trace)."""
    validate(reference, capacity)

    frames = []
    last_used = {}
    hits = 0
    faults = 0
    trace = []

    for position, page in enumerate(reference):
        if page in frames:
            hits += 1
            status = "H"
        else:
            faults += 1
            status = "F"
            if len(frames) < capacity:
                frames.append(page)
            else:
                victim = min(frames, key=lambda item: last_used[item])
                index = frames.index(victim)
                frames[index] = page
        last_used[page] = position
        trace.append((page, frames[:], status))

    return hits, faults, trace


def optimal(reference, capacity):
    """Optimal (Belady) replacement. Returns (hits, faults, trace)."""
    validate(reference, capacity)

    frames = []
    hits = 0
    faults = 0
    trace = []

    for position, page in enumerate(reference):
        if page in frames:
            hits += 1
            status = "H"
        else:
            faults += 1
            status = "F"
            if len(frames) < capacity:
                frames.append(page)
            else:
                future = reference[position + 1:]
                distances = []
                for loaded in frames:
                    if loaded in future:
                        distances.append(future.index(loaded))
                    else:
                        distances.append(float("inf"))
                victim_index = max(
                    range(len(frames)), key=lambda i: distances[i]
                )
                frames[victim_index] = page
        trace.append((page, frames[:], status))

    return hits, faults, trace


def show(name, result, total):
    """Print the trace and the statistics of one strategy."""
    hits, faults, trace = result
    print(f"\n{name}")
    for page, frames, status in trace:
        print(f"{page} -> {frames} {status}")
    print("Hits:", hits)
    print("Faults:", faults)
    print("Hit ratio:", round(hits / total, 3))
    print("Fault ratio:", round(faults / total, 3))


reference = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
capacity = 3

show("FIFO", fifo(reference, capacity), len(reference))
show("LRU", lru(reference, capacity), len(reference))
show("Optimal", optimal(reference, capacity), len(reference))

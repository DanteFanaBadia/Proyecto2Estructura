
def binary_search(objs, min_idx, max_idx, term, key):
    while min_idx <= max_idx:
        mid_idx = min_idx + (max_idx - min_idx) // 2
        if getattr(objs[mid_idx], key) == term:
            return objs[mid_idx]
        elif getattr(objs[mid_idx], key) > term:
            max_idx = mid_idx - 1
        else:
            min_idx = mid_idx + 1
    return None

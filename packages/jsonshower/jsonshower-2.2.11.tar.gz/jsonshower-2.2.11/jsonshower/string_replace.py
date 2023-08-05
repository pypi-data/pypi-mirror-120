import re
import warnings
from fuzzysearch import find_near_matches

def fuzzy_match(needle, hay, flags=re.DOTALL, needle_length_window=0.2):
    """Searches on the most similar string. 
    Code adapted from: 
    https://stackoverflow.com/questions/17740833/checking-fuzzy-approximate-substring-existing-in-a-longer-string-in-python/31433394#31433394
    """
    try:
        matched = re.search(needle, hay, flags=flags)
    except:
        pass
    if matched is not None:
        return matched
    try:
        gen = list(find_near_matches(needle, hay, max_l_dist=5))
        if len(gen) > 0:
            return gen[0]
    except (StopIteration, RuntimeError):
        return

def get_start_end_index(achievement, rel_string, case_insensitive=False):
    rel_string = rel_string.strip()
    if case_insensitive:
        matched = fuzzy_match(rel_string, achievement, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    else:
        matched = fuzzy_match(rel_string, achievement)
    if matched is None:
        warnings.warn(rel_string + "\nnot found in: \n" + achievement)
        return {"start_index": -1, "end_index": -1, "repl": rel_string}
    if hasattr(matched, "regs"):
        return {"start_index": matched.regs[0][0], "end_index": matched.regs[0][1], "repl": rel_string}
    elif hasattr(matched, "start"):
        return {"start_index": matched.start, "end_index": matched.end, "repl": rel_string}

def get_all_start_end_indexes(original_text: str, to_replace: list,
    start_hooks: list, end_hooks: list, case_insensitive: bool=False):
    all_indexes = [get_start_end_index(original_text, r, case_insensitive) for r in to_replace if r != ""]
    [i.update({
        "start_hook": start_hooks[counter],
        "end_hook": end_hooks[counter]}) for counter, i in enumerate(all_indexes)]
    sorted_indexes = sorted(all_indexes, key=lambda x: x["end_index"], reverse=True)
    sorted_indexes = sorted(sorted_indexes, key=lambda x: x["start_index"], reverse=True)
    start_indexes = []
    for i in sorted_indexes:
        start_indexes = [i["start_index"] for i in sorted_indexes]
        end_indexes = [i["end_index"] for i in sorted_indexes]
        sorted_start_hooks = [i['start_hook'] for i in sorted_indexes]
        sorted_end_hooks = [i['end_hook'] for i in sorted_indexes]
    return {
        "start_indexes": list(start_indexes), 
        "end_indexes": list(end_indexes),
        "all_indexes": sorted_indexes,
        "sorted_start_hooks": sorted_start_hooks,
        "sorted_end_hooks": sorted_end_hooks,
        "flat_index": sorted(start_indexes + end_indexes, reverse=True)
    }

def inject_string(string, repl, start_index, end_index):
    return string[:start_index] + repl + string[end_index:]

def inject_strings_from_index_info(index_info, output, start_hooks, end_hooks):
    start_index_counter = 0
    end_index_counter = 0
    for counter, i in enumerate(index_info['flat_index']):
        if i in index_info['end_indexes']:
            if i != -1:
                output = inject_string(
                    output, index_info['sorted_end_hooks'][end_index_counter], i, i)
            index_info['end_indexes'].remove(i)
            end_index_counter += 1
        elif i in index_info['start_indexes']:
            if i != -1:
                output = inject_string(
                    output, index_info['sorted_start_hooks'][start_index_counter], i, i)
            index_info['start_indexes'].remove(i)
            start_index_counter += 1
    return output

def inject_strings(string, repls, start_hooks: list, end_hooks: list, 
    case_insensitive: bool=False):
    index_info = get_all_start_end_indexes(string, repls, start_hooks, end_hooks,
        case_insensitive=case_insensitive)
    return inject_strings_from_index_info(
        index_info, string, start_hooks, end_hooks
    )

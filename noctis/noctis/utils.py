"""
utilities for noctis. Simple tools and extras.
"""

def get_username(request):
    username = None
    if request.user.is_authenticated():
        return request.user.username
    else:
        raise "User doesn't exist."

def slicedict(d, s):
    '''
    Slice and return the k,v pairs that match out 's'
    parameter.
    '''
    return {k:v for k,v in d.items() if k.startswith(s)}

def merge_dicts(dict1, dict2):
    '''
    Merge dictionaries recessively and pass back the result.
    If a conflict of types arrive, just get out with what
    we can.
    '''
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(merge_dicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])

def clean_query(values, SPLIT="__"):
    '''
    Returns a clean map of the values by recursively pushing our values
    to dictionaries. Auto assume multi-key bases as their id.

    For fast database retrieval and push back but perhaps not the fastest.
    It may be faster to run an in-line model -> dict function. This is just for
    convenience.

    @params
    values : dict : the return of a query set with one set of keys

    SPLIT : str : the split determination.
    '''
    def make_dict_from_item(base, rest, value):
        ''' Make a dict out of our k(split) v pair '''
        if base:
            rest[base[0]] = make_dict_from_item(base[1:], {}, value)
        else:
            rest = value
        return rest

    out_ = {}
    for a_key, a_value in values.items():
        if SPLIT in a_key:
            ## If the split is in the key we can push it back as a dict to merge.
            split_context = a_key.split(SPLIT)

            ## This will return us { "k1" : { 'sk1' : { 'ssk1' : v1 } } }
            _tmp = make_dict_from_item(split_context, {}, a_value)

            if split_context[0] in out_.keys():
                if isinstance(out_[split_context[0]], dict):
                    out_[split_context[0]].update(merge_dicts(out_[split_context[0]], _tmp[split_context[0]]))
            else:
                ## If we don't have a key yet we should set on (assume id)
                ## Then update our merge to be ready.
                if isinstance(a_value, int):
                    out_[split_context[0]] = { 'id' : a_value }
                elif isinstance(a_value, str):
                    out_[split_context[0]] = { split_context[-1] : a_value }
                out_.update(_tmp)
        elif a_key in out_.keys():
            ## if the values have been pushed to that dict already...
            if isinstance(a_value, int):
                _tmp = { "id" : a_value }
            else:
                ## Shouldn't happen. Avoid breakdown.
                _tmp = { "some_val" : a_value }
            out_[a_key].update(_tmp)
        elif len(slicedict(values, a_key)) > 1:
            ## If there are multiple values we should still try to create
            ## that key entry. Don't combine with previous elif for performance
            ## reasons
            if isinstance(a_value, int):
                _tmp = { "id" : a_value }
            else:
                ## Shouldn't happen. Avoid breakdown.
                _tmp = { "some_val" : a_value }
            out_[a_key].update(_tmp)
        else:
            ## If it's the only one, leave it alone.
            out_[a_key] = a_value
    return out_
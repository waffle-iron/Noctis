"""
utilities for noctis. Simple tools and extras.
"""

from copy import deepcopy

def get_username(request):
    username = None
    if request.user.is_authenticated():
        return request.user.username
    else:
        raise "Username doesn't exist."

def slicedict(d, s):
    return {k:v for k,v in d.items() if k.startswith(s)}

def subdict(fk, sfk, d):
    return {k[len(fk+2):]:v for k,v in d.items() if k.startswith(fk) and k[len(fk+2):].startswith(sfk)}

def organize_values(fks, values, SPLIT="__"):
    '''
    Creating an organized dictionary from the elements in a
    QuerySet. Continually modify our return until all SPLIT
    elements have been satisfied.

    @params
    fks : list : all of the Foreign Keys we'll be organizing

    values : dict : values to organize with.

    SPLIT : str : What the incoming data will be split by. !Caution!

    ### TODO: NOT FINISHED. Needs another pass. A lot of moving parts.
    '''

    ##  ['vc'] -> { 'vc' : 1 ... 'vc_at_n' : 'test' }
    for a_fk in fks:
        ## { 'vc' : 1, 'vc_at_n': 'test' }
        _sub_vals = slicedict(values, a_fk)
        if _sub_vals:
            if not isinstance(values.get(a_fk), dict):
                if isinstance(values.get(a_fk), int):
                    ## { ... 'vc' : { 'id' : 1 } ... }
                    values[a_fk] = dict(id=values[a_fk])
                else:
                    values[a_fk] = {}
            for _a_sub_val in _sub_vals:
                if _a_sub_val != a_fk:
                    _potential_key = _a_sub_val.split(SPLIT, 1)[1:]
                    print ("POTKEY : ", _potential_key)
                    if SPLIT in _potential_key and not values[a_fk].get(_potential_key):
                        print ("SUBDICT: ", subdict(a_fk, [_potential_key], values))
                        org = { _potential_key : organize_values(_potential_key,
                                                                 subdict(a_fk,
                                                                         _potential_key,
                                                                         values
                                                                        ),
                                                                 SPLIT
                                                                )
                              }
                        values[a_fk].update(org)
                    else:
                        print ()
                        print("Values: ", values)
                        print ()
                        _split_sub_val = _a_sub_val.split(SPLIT)
                        if not values[a_fk].get(_split_sub_val[0]):
                            values[a_fk].update( { _split_sub_val[0] : values.pop(_split_sub_val[0]) } )
        return values
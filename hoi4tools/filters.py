#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from optparse import OptionParser
import fnmatch
import os
import sys
import re
import json

from pprint import pprint
import ply.lex as lex
import ply.yacc as yacc

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

# merge two dicts together up to a depth of 2 (dict of dict merge)
# TODO will crash and burn if "z[i]" is not a dictionary
def merge_two_dicts_depth2(x,y):
    z = x.copy()   # start with x's keys and values
    for i in y:
        if i not in z:
            z[i] = y[i]
        else:
            for j in y[i]:
                z[i][j] = y[i][j]
    return z

# extract the bites that interest us for the production optimizer
def filter_production(data):
    ret = {'unit': {}, 'equipement': {}}

    archetype_list = set([])

    # scan units
    for s in data['sub_units']:
        if 'group' in data['sub_units'][s]:
            sub_unit = data['sub_units'][s]
            group = data['sub_units'][s]['group']

            if group not in ret['unit']:
                ret['unit'][group] = {}
            ret['unit'][group][s] = {
                    'need': sub_unit['need']
            }
            for a in data['sub_units'][s]['need']:
                archetype_list.add(a)

    # scan for equipement
    archetype_list2 = set([])
    for s in data['equipments']:
        equipement = data['equipments'][s]
        if 'archetype' in equipement and \
            equipement['archetype'] in archetype_list and \
            'year' in equipement:
                year = equipement['year']
                archetype = equipement['archetype']
                if 'build_cost_ic' in equipement:
                    build_cost_ic = equipement['build_cost_ic']
                else:
                    build_cost_ic = data['equipments'][archetype]['build_cost_ic']

                if year not in ret['equipement']:
                    ret['equipement'][year] = {}
                ret['equipement'][year][archetype] = {'cost': float(build_cost_ic)}
                archetype_list2.add(archetype)

    if archetype_list2 != archetype_list:
        raise Exception("failed to recover all the equipement types")
    return ret

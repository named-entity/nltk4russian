# -*- coding: utf-8 -*-
"""RusCorpora -> OpenCorpora tag conversion.
A single RNC analysis (a number of tags) is given as the input argument, the result is a converted OC 'analysis'.
This script does not handle some cases such as those involving semantic tags.

Example:
    >>> print convert_rnc_oc('V,ipf,intr,act=partcp,f,sg,gen,praet')
    PRTF,impf,intr,past,actv femn,sing,gent
"""

import codecs
from collections import OrderedDict


def parse_rules(rules_file):
    """Parse the file with a list of rules and return an ordered dictionary.

    :param rules_file: a list of rules in form of 'RNC => OC' on each line, in .txt format, encoded in UTF-8.
    :return: ordered dictionary corresponding to the lines in the input rules file.
    """
    rules_lines = []
    with codecs.open(rules_file, 'r', 'utf-8') as raw_rules:
        rules_text = raw_rules.read()
    for line in rules_text.split('\r\n'):
        rules_lines.append(line)
    temp_list = []
    for line in rules_lines:
        if line == '' and line.startswith('#'):
            continue
        if len(line.split(' => ')) == 2:
            temp_list.append([frozenset(line.split(' => ')[0].split(',')), line.split(' => ')[1].split(',')])
    rules_dict = OrderedDict(temp_list)
    return rules_dict


rules_dict = parse_rules('rules.txt')
"""Using one general dictionary which is copied with every other analysis."""


def convert_tags(rules_dict, original_list):
    """Convert given analysis and return a set of corresponding OC tags (no specific order).

    :param rules_dict: ordered dictionary corresponding to the lines in the rules file.
    :param original_list: list of split tags in the original analysis.
    :return: list of OC tags converted from the original RNC.
    """
    resulting_tags = []
    original_set = set(original_list)
    for before_set in rules_dict.keys():
        if before_set & original_set == None:
            continue
        if before_set <= original_set:
            resulting_tags.append(rules_dict[before_set])
            original_set -= before_set & original_set
            if before_set != set('='):
                for separate_tag in before_set:
                    if separate_tag in rules_dict:
                        rules_dict.pop(separate_tag, None)
                rules_dict.pop(before_set, None)
    return sum(resulting_tags, [])


def convert_rnc_oc(rus_tag):
    """Convert a single RNC analysis and return the corresponding OC 'analysis'.

    :param rus_tag: the original single RNC analysis.
    :param rules_dict: an ordered dictionary corresponding to the lines in the rules file.
    :return: a string of OC tags.
    """
    # pl= - Pluralia tantum
    grammeme_list = rus_tag.replace('pl=', 'plt=').replace('=', ',=,').split(',')
    temp_rules_dict = OrderedDict(rules_dict)
    """The dictionary is copied so that the entries could be re-used."""
    result = convert_tags(temp_rules_dict, grammeme_list)
    if result:
        new_pos = [tag for tag in result if tag.isupper()]
        if len(new_pos) == 1:
            set_pos(new_pos[0])
    else:
        pass
    sorted_grammemes = sorted(result, key=sort_weight)
    result = ','.join(sorted_grammemes).replace('|', ' ').replace(', ,', ' ').replace(', ', '').replace(' ,',
                                                                                                        '').replace('   ', ' ')
    """Sometimes there may be two '='s in an RNC analysis, so it should be checked that there are no redundant spaces."""
    if result == '':
        return 'UNKN'
    return result


pos = None
"""Variable for using POS globally."""


def set_pos(tag):
    """Set the global variable to the given POS tag.

    :param tag: the POS of the word in question.
    """
    global pos
    pos = tag


def sort_weight(tag):
    """Technical function which has to be used as key while sorting."""
    tag_weight = get_weight(tag)
    return tag_weight


def get_weight(tag):
    """Get the position of a single tag (used as key function while sorting).

    :param tag: One OC tag
    :return: the position number of the tag in the list of all possible combinations.
    """
    tag_weight = 0
    for category in tags:
        if tag in tags[category]:
            if pos in non_standard_order:
                """Check that some categories (not from the list) won't show up for some POS (e.g. Pltm for NPRO)"""
                if category in non_standard_order[pos]:
                    tag_weight = non_standard_order[pos].index(category)
            else:
                tag_weight = standard_order.index(category)
            break
    return tag_weight


standard_order = ['POST', 'SUBX', 'APRO', 'ANPH', 'ASPECT', 'TRAN', 'PERSON', 'TENSE', 'VOICE', 'MOOD', 'INVL', 'ANIM',
                  'PRNT', 'FIXD', 'delimiter', 'GENDER', 'NUMBER', 'CASE', 'ABBR']
"""General order used for all tags, unless otherwise speicified."""

non_standard_order = {
    'PRTF': ['POST', 'SUBX', 'ASPECT', 'TRAN', 'TENSE', 'VOICE', 'ANIM', 'delimiter', 'GENDER', 'NUMBER', 'CASE', ],
    'VERB': ['POST', 'ASPECT', 'TRAN', 'delimiter', 'VOICE', 'GENDER', 'NUMBER', 'PERSON', 'TENSE', 'MOOD',
             'INVL', 'CASE', ],
    'NOUN': ['POST', 'ANIM', 'GENDER', 'TANTUM', 'PNAME', 'MF', 'FIXD', 'NAME', 'ABBR', 'INIT', 'delimiter', 'NUMBER',
             'CASE', ],
    'GRND': ['POST', 'ASPECT', 'TRAN', 'delimiter', 'TENSE', ],
    'ADJF': ['POST', 'FIXD', 'SUBX', 'APRO', 'ANPH', 'ANIM', 'delimiter', 'GENDER', 'PERSON', 'NUMBER', 'CASE',
             'ABBR', ],
    'NPRO': ['POST', 'GENDER', 'PERSON', 'ANPH', 'ANIM', 'FIXD', 'delimiter', 'NUMBER', 'CASE', 'ABBR', ]
}
"""Specific order for some POS which notably have some differences."""

tags = {
    'POST': (
        'NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND', 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP',
        'CONJ', 'PRCL', 'INTJ', 'INIT', ),
    'SUBX': ('Subx', ),
    'ABBR': ('Abbr', ),
    'INIT': ('Init'),
    'TANTUM': ('Sgtm', 'Pltm', ),
    'NAME': ('Patr', 'Surn', ),
    'PNAME': ('Name', ),
    'GENDER': ('GNdr', 'femn', 'neut', 'masc', ),
    'MF': ('Ms-f', 'Inmx', ),
    'PRNT': ('Prnt', ),
    'INVL': ('incl', 'excl', ),
    'ANIM': ('ANim', 'anim', 'inan', ),
    'NUMBER': ('sing', 'plur', ),
    'FIXD': ('Fixd', ),
    'CASE': ('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen1', 'gen2', 'acc2', 'loc2', ),
    'ASPECT': ('perf', 'impf', ),
    'TRAN': ('tran', 'intr', ),
    'VOICE': ('actv', 'pssv', ),
    'MOOD': ('indc', 'impr', ),
    'TENSE': ('pres', 'past', 'futr', ),
    'PERSON': ('1per', '2per', '3per', ),
    'APRO': ('Apro', 'Anum', ),
    'ANPH': ('Anph', ),
    'delimiter': ('|', )
}
"""Dictionary of all useful OC tags while comparing their order."""

# def test():
# # лежавшей V,ipf,intr,act=partcp,f,sg,gen,praet	PRTF,impf,intr,past,actv femn,sing,gent
# rnc = 'V,ipf,intr,act=partcp,f,sg,gen,praet'
#     oc = 'PRTF,impf,intr,past,actv femn,sing,gent'
#     test = convert_rnc_oc(rnc)
#     print oc == test


# if __name__ == '__main__':
#     test()
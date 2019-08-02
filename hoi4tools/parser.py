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

WINDOWS_LINE_ENDING = '\r\n'
UNIX_LINE_ENDING = '\n'

# List of token names for the hoi4 files
tokens = (
  'EQUAL',
  'LBRACKET',
  'RBRACKET',
  'LT',
  'GT',
  'STRING',
  'NUMBER',
  'QUOTED_STRING'
)

# content example
#
# stuff = {
#         foo = {
#             biture = sanglier
#             cost = 0.42
#             power > 9000
#             chance < 13.5
#             modifier = -0.7
#         }
#         bar = {
#             item1
#             item2
#             "item3 with quote"
#         }
#
# }

### utilitary functions
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

def Hoi4Lexer():

    # Regular expression rules for simple tokens
    t_EQUAL      = r'='
    t_LBRACKET   = r'{'
    t_RBRACKET   = r'}'
    t_LT         = '<'
    t_GT         = '>'
    t_STRING     = r'[A-Za-z0-9_]+'

    # matching for quoted string (only works if string is on one line)
    def t_QUOTED_STRING(t):
        r'\"([^\\\"]|\\.)*\"'
        t.value = t.value[1:-1]
        return t

    # matching for numbers
    def t_NUMBER(t):
        r'[-\d\.]+'
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore  = ' \t'

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        print("'%s'" % t.value[0])
        print(t.value[0])
        t.lexer.skip(1)

    # Build the lexer from my environment and return it
    return lex.lex()

def Hoi4Yaccer():

    Hoi4Lexer()

    # match for stuff = <SOMETHING>
    def p_allocation(p):
        '''allocation : STRING EQUAL STRING
                      | STRING EQUAL list
                      | STRING EQUAL dict
                      | STRING EQUAL NUMBER
                      | STRING GT NUMBER
                      | STRING LT NUMBER
                      | STRING EQUAL QUOTED_STRING
        '''
        if p[2] == '=':
            p[0] = {p[1]: p[3]}
        else:
            # paradox format allows for inequalities, which doesn't map cleanly into json
            # but these are pretty rare (seen only for radar and sonar slots count on ships)
            # so we put them in a special format
            p[0] = {p[1]: {'operation': p[2], 'value': p[3]}, 'META': 'INEQ'}

    # match for { stuff1 stuff2 stuff3 }
    def p_list(p):
        '''list : LBRACKET string_items RBRACKET
        '''
        p[0] = p[2]

    # match for { }
    def p_empty_list(p):
        "list : LBRACKET RBRACKET"
        p[0] = []

    # match for 'stuff1 stuff2 stuff3' (content of { stuff1 stuff2 stuff3 })
    def p_elements(p):
        '''string_items : STRING string_items
                        | QUOTED_STRING string_items
        '''
        p[2].append(p[1])
        p[0] = p[2]

    # termination for previous
    def p_element_single(p):
        '''string_items : STRING
                        | QUOTED_STRING
        '''
        p[0] = [p[1]]

    # match for:
    # {
    #    stuff1 = <SOMETHING>
    #    stuff2 = <SOMETHING_ELSE>
    # }
    def p_dict(p):
        '''dict : LBRACKET allocation_items RBRACKET'''
        p[0] = p[2]

    # match for content of previous:
    #    stuff1 = <SOMETHING>
    #    stuff2 = <SOMETHING_ELSE>
    def p_allocation_items(p):
        '''allocation_items : allocation allocation_items'''
        p[0] = merge_two_dicts(p[1], p[2])

    # termination of previous
    def p_allocation_single(p):
        '''allocation_items : allocation'''
        p[0] = p[1]

    def p_error(p):
        print("Syntax error at '%s'" % p.value)

    return yacc.yacc(debug=0, write_tables=0)

def walk(directory):
    """Walk a given directory to recover interesting hoi4 files"""
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.txt'):
            if not re.match(r'.*names.*', root):
                matches.append(os.path.join(root, filename))
    return matches

def _open_crlf_lf(in_file):
    """Open a file, switching to LF and removing comments"""
    with open(in_file, "r") as fh:
        # we replace CRLF by CF and remove comments
        return re.sub(r'#.*', '', fh.read().replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING))

# debug function to visualize the tokenization
def _lex_file(in_file, data):
    lexer = Hoi4Lexer()
    lexer.input(_open_crlf_lf(in_file))
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# parse a file and return a dictionnary
def parse_file(in_file):
    """Parse a given txt hoi4 file"""
    parser = Hoi4Yaccer()
    return parser.parse(_open_crlf_lf(in_file))


def parse_dir(directory):
    """Analyze all the interesting files in a directory"""
    matches = walk(directory)
    data = {}
    for in_file in matches:
        ret = parse_file(str(in_file))
        data = merge_two_dicts_depth2(data, ret)
    return data

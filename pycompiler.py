#!/usr/bin/env python3

from lark import Lark, Transformer

#
# lang_parser = Lark(r"""
#     start: expr+
#     expr: SIGNED_NUMBER add_op expr | SIGNED_NUMBER
#
#     div_op: "/"
#     sub_op: "-"
#     mul_op: "*"
#     add_op: "+"
#
#     %import common.WS
#     %import common.SIGNED_NUMBER
#     %ignore WS
# """)
#
# print(lang_parser.parse('1 + 2').pretty())


json_grammar = r'''
    ?value : dict
           | list
           | string
           | SIGNED_NUMBER  -> number
           | "true"         -> true
           | "false"        -> false
           | "null"         -> null

    list : "[" [value ("," value)*] "]"
    
    dict : "{" [pair ("," pair)*] "}"
    pair : string ":" value
    
    string : ESCAPED_STRING
    
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    
    %ignore WS
'''

json_parser = Lark(json_grammar, start='value', parser='lalr')
text = '{"key": ["item0", "item1", 3.14, true]}'
tree = json_parser.parse(text)
print( tree.pretty() )


class MyTransformer(Transformer):
    def list(self, items):
        return list(items)

    def pair(self, items):
        k, v = items
        return k, v

    def dict(self, items):
        return dict(items)


print( MyTransformer().transform(tree) )


class TreeToJson(Transformer):
    def string(self, s):
        return s[0][1:-1]

    def number(self, n):
        return float(n[0])

    list = list
    pair = tuple
    dict = dict

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False

print( TreeToJson().transform(tree) )

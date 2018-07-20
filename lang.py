#!/usr/bin/env python3

from lark import Lark

TEXT = 'number = 2 * (4 + 2)'

PRIMITIVES = '''
i32
i64
u32
u64
byte
string

'''

EXAMPLE = '''
import package.package.function
import package.type
import package.interface
import package, package, otherstuff

struct Object
    name : type
    ...
    
interface Name
    func definition ...
    func ...
    
implement Interface : Type
    func ...
        implementation
        ...

func functionName[Generic] (identifier : [[ref] [mut] type] | Interface, ...) : return_type
    let object1 : Object        # immutable object on stack
    let mut object2 : Object    # mutable object on stack
    ref object3 : Object        # immutable object on heap
    ref mut object4 : Object    # mutable object on heap
'''

AST = '''
Function
    name
    parameters [list]
    return type

Parameter
    name
    type

Identifier
    name
    type
    
Operators
    + add
    - subtract
    * multiply
    / divide
    % modulus
    ^ exponent
    . access operator

Keywords
    ref
    let
    mut
    interface
    func
    implement
    assert

Type
    ref or stack
'''


grammar = '''
start : sum
    | NAME "=" sum  -> assign_stmt

sum : product
    | sum "+" product   -> add
    | sum "-" product   -> sub

product : atom
    | product "*" atom  -> mul
    | product "/" atom  -> div

atom : NUMBER       -> number
    | "-" atom      -> neg
    | NAME          -> var
    | "(" sum ")"

%import common.CNAME    -> NAME
%import common.NUMBER
%import common.WS

%ignore WS
'''

parser = Lark(grammar)
tree = parser.parse(TEXT)
print(tree.pretty())

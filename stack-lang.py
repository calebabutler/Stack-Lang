import math
import copy
import sys

def in_defs(token, defs):
    for pair in defs:
        if pair[0] == token:
            return True
    return False

def get_def(token, defs):
    for i in range(-1, -1 * len(defs) - 1, -1):
        if defs[i][0] == token:
            return defs[i][1]

def is_num(char):
    if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return True
    else:
        return False

def compute(tokens, stack = None, defs = None, funs = None):
    if stack is None:
        stack = []
    if defs is None:
        defs = []
    if funs is None:
        funs = []
    for token in tokens:
        if isinstance(token, list):
            stack.append(token)
        elif is_num(token[0]):
            stack.append(float(token))

        elif token == "dup":
            stack.append(stack[-1])
        elif token == "exch":
            z = stack[-2]
            stack[-2] = stack[-1]
            stack[-1] = z
        elif token == "pop":
            stack.pop()
        elif token == "stack->list":
            stack.append(stack)

        elif token == "+":
            arg2 = stack.pop()
            arg1 = stack.pop()
            stack.append(arg1 + arg2)
        elif token == "-":
            arg2 = stack.pop()
            arg1 = stack.pop()
            stack.append(arg1 - arg2)
        elif token == "*":
            arg2 = stack.pop()
            arg1 = stack.pop()
            stack.append(arg1 * arg2)
        elif token == "/":
            arg2 = stack.pop()
            arg1 = stack.pop()
            stack.append(arg1 / arg2)
        elif token == "%":
            arg2 = stack.pop()
            arg1 = stack.pop()
            stack.append(arg1 % arg2)
        elif token == "floor":
            stack.append(math.floor(stack.pop()))

        elif token == "=":
            if stack.pop() == stack.pop():
                stack.append("t")
            else:
                stack.append("f")
        elif token == "<":
            if stack.pop() > stack.pop():
                stack.append("t")
            else:
                stack.append("f")
        elif token == ">":
            if stack.pop() < stack.pop():
                stack.append("t")
            else:
                stack.append("f")

        elif token == "type":
            arg = stack.pop()
            if isinstance(arg, list):
                stack.append("list")
            elif isinstance(arg, float):
                stack.append("number")
            else:
                stack.append("symbol")
        elif token == "first":
            arg = stack.pop()
            stack.append(arg[0])
        elif token == "rest":
            arg = stack.pop()
            stack.append(arg[1:])
        elif token == "pair":
            arg2 = stack.pop()
            arg1 = stack.pop()
            stack.append([arg1] + arg2)

        elif token == "concat":
            arg2 = stack.pop()
            arg1 = stack.pop()
            stack.append(arg1 + arg2)

        elif token == "print":
            print(stack.pop())

        elif token == "if":
            pred2 = stack.pop()
            pred1 = stack.pop()
            cond = stack.pop()
            if cond == "t":
                compute(pred1, stack, defs, funs)
            elif cond == "f":
                compute(pred2, stack, defs, funs)
            else:
                stack.append(cond)
                stack.append(pred1)
                stack.append(pred2)
        elif token == "!":
            compute(stack.pop(), stack)

        elif token == "def":
            arg2 = stack.pop()
            arg1 = stack.pop()
            defs.append([arg1, arg2])
        elif token == "popdef":
            defs.pop()

        elif token == "defun":
            arg2 = stack.pop()
            arg1 = stack.pop()
            funs.append([arg1, arg2])
        elif token == "popfun":
            funs.pop()

        elif token[0] == "'":
            stack.append(token[1:])
        else:
            if in_defs(token, funs):
                compute(get_def(token, funs), stack, defs, funs)
            elif in_defs(token, defs):
                stack.append(get_def(token, defs))
            else:
                stack.append(token)

def parenthesize(lst, configured = None):
    if configured is None:
        lst.insert(0, '(')
        lst.append(')')
        return parenthesize(lst, True)
    if len(lst) == 0:
        return []
    token = lst.pop(0)
    if token == '(':
        L = []
        while lst[0] != ')':
            L.append(parenthesize(lst, True))
        lst.pop(0)
        return L
    elif token == ')':
        return []
    else:
        return token

def stringisize(lst):
    i = 0
    string = ""
    tokens = []
    while i < len(lst):
        if lst[i][0] == '"':
            if lst[i][-1] != '"':
                string += lst[i][1:]
                i += 1
                while lst[i][-1] != '"':
                    string += " "
                    string += lst[i]
                    i += 1
                string += " "
                string += lst[i][:-1]
            else:
                string += lst[i][1:-1]
            tokens.append(string)
            string = ""
        else:
            tokens.append(lst[i])
        i += 1
    return tokens

def tokenize(code):
    uncommented = ""
    comment = False
    for character in code:
        if character == ';':
            comment = True
        elif character == '\n':
            uncommented += '\n'
            comment = False
        elif comment is False:
            uncommented += character
    return uncommented       \
        .replace('(', ' ( ') \
        .replace(')', ' ) ') \
        .split()

def parse(code):
    return parenthesize(stringisize(tokenize(code)))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        compute(parse(open(sys.argv[1], 'r').read()))
    else:
        stack = []
        defs = []
        funs = []
        while True:
            line = input("> ")
            if line == "quit" or line == "q" or line == "exit":
                exit()
            compute(parse(line), stack, defs, funs)
            print(stack)

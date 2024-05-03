#!/usr/bin/python3
# -*- coding: utf-8 -*-


import re
import random as r
import string

# keep track of randomly generated strings in case two have the same name
RANDOM_STRINGS = set()


def rand_name_gen(length=10):
    global RANDOM_STRINGS
    rnd = "".join([r.choice(string.ascii_letters) for _ in range(length)])
    while rnd in RANDOM_STRINGS:
        rnd = "".join([r.choice(string.ascii_letters) for _ in range(length)])
    return rnd

def rand_name_gen2(script):
    """48-57 0-9, 65-90 A-Z, 97-122 a-z"""
    c = list(range(97, 122+1))+list(range(65, 90+1))
    rnd = [0]
    while 1:
        new = "".join(map(lambda x: chr(c[x]), rnd))
        if new not in script:
            yield new
        rnd[0] += 1
        for i in range(len(rnd)):
            if rnd[i] >= len(c):
                rnd[i] = 0
                try:
                    rnd[i+1] += 1
                except IndexError:
                    rnd.append(0)

def get_indent(line):
    i = 0
    while line[i] == ' ':
        i += 1
    return i

def get_script(path):
    with open(path, 'r') as file:
        script = file.read()
    return script

def write_script(path, script):
    with open(path+'.new', 'w') as file:
        file.write(script)

def purge_spaces(script):
    """Spaces before newline and spaces between '=,)' """
    s = re.sub(r' +\n', r'\n', script)
    s = re.sub(r'( )*(,|=|!=|==|<|>|<=|>=|-=|\+=|\*=|\\=|\\\\=|%=)( )*', r'\2', s)
    return re.sub('\n{2,}', '\n', s)

def get_modules(script):
    pass

def delete_comments(script):
    """Delete comments except #!/usr/bin/python and # -*- coding: utf-8 -*-"""
    return re.sub(r' *#(?!!/usr/bin/python| -\*- coding: utf-8 -\*-).*(?=\n)', '', script)

def join_similar_line(script):
    """
    module.function1()      =>      module.function1();module.function2()
    module.function2()
    a=1                     =>      a=1;b=2
    b=2
    """
    indents = []
    splitedLines = script.split('\n')
    newScript = splitedLines[0]
    lastLine = splitedLines[0]
    for i in range(1, len(splitedLines)):
        line = splitedLines[i]
        # variable assignement or function call
        # if useless line, add it
        if not re.match(r'^( *)\w+([\.,\-\w\[\]])*=', line) and\
           not re.match(r'^( *)\w+(\.\w*)*\(.*\)', line):
            newScript += '\n' + line
        # if good line and previous on same indent, join them
        elif (re.match(r'^( *)\w+([\.,\-\w\[\]])*=', lastLine) or\
              re.match(r'^( *)\w+(\.\w*)*\(.*\)', lastLine)) and\
              get_indent(line) == get_indent(lastLine):
            newScript += ';' + line.lstrip(' ')
        else:
            newScript += '\n' + line
        lastLine = line
    return newScript

def get_global_var(script):
    gVars = []
    for mtch in re.finditer(r'(?<=\n)(\w+) ?= ?(.*)\n', script):
        gVars.append(mtch.groups())
    return gVars

def replace_global_var(script):
    #for variable, value in get_global_var(script):
    #    # we don't want to change the (re)assignated ('=') version
    #    script = re.sub(r'\b'+variable+r'\b(?![\.=])', value, script)
    return script

def one_line(script):
    """
    FROM             |     TO
    a = [1, 2, 3,    |     a = [1, 2, 3, 4, 5, 6]
         4, 5, 6]    |
    if a and b and\  |     if a and b and c and d:
       c and d:      |
    if a>0:          |     
        fn1_call()   |     if a>0: fn1_call()
    else:            |     else: fn2_call()
        fn2_call()   |     
    for i in xyz:    |     for i in xyz: x += i
        x += i       |
    To do only once to avoid messing with nested statements and loops
    """
    # one line containers
    n = 1
    while n > 0: # when containers are splitted on several lines
        script, n = re.subn(r'(.+,)(\n *)(.+)', r'\1 \3', script)
    # \breakline
    script = re.sub(r'\\\n *', ' ',script)
    # one line for, if, elif and while
    script = re.sub(r'( *)((for|if|elif|while) .*:)\n( )+(.*\n)(?=\1[^\s])', r'\1\2 \5', script)
    # one line else
    script = re.sub(r'( *)(else:)\n( )*(.*\n)(?=\1[^ ])', r'\1\2 \4', script)

    return script

def get_functions(script):
    functions = {}
    regexC = r'(    )*?def (\w+)\((.*?)\):\n(\1+(\"\"\".*?\"\"\"\n)?.*?)(?=\n\1?\w)'
    regexG = r'(?<=\n)def (\w+)\((.*?)\):\n((\"\"\".*?\"\"\"\n)?.*?)(?=\n\w)'
    parts = ("indent", "name", "args", "body", "doc")
    # for function inside classes
    for mtch in re.finditer(regexC, script, flags=re.DOTALL):
        name = mtch.group(2)
        functions[name] = {"range":(mtch.start(), mtch.end())}
        functions[name].update(zip(parts, mtch.groups()))
        functions[name]["whole"] = script[mtch.start():mtch.end()]
    # for functions outside classes
    for mtch in re.finditer(regexG, script, flags=re.DOTALL):
        name = mtch.group(1)
        functions[name] = {"range":(mtch.start(), mtch.end())}
        functions[name].update(zip(parts[1:], mtch.groups()))
        functions[name]["indent"] = ''
        # from indent+def to the end of the function
        functions[name]["whole"] = script[mtch.start():mtch.end()]
    return functions

def extract_arguments(function):
    """Return the arguments passed to the function and a random new name"""
    args = []
    for arg in function["args"].split(','):
        arg = arg.strip(' ')
        if re.match(r'^\w+=', arg): # '=' after the name
            args.append(arg[:arg.index("=")])
        elif arg.startswith('*'): # * or **
            args.append(arg[1:])
        elif arg != '':
            args.append(arg)
    return [(a, next(randGen)) for a in args]

def replace_functions(script):
    """Change the body of the function with new variable names"""
    functions = get_functions(script)
    # each substitution should be done separately, in the same order
    # replace each argument with the new one
    for k, v in functions.items():
        newArgs = extract_arguments(v)
        newBody = v["whole"]
        oldBody = newBody
        for na in newArgs:
            newBody = re.sub(r'(?<=[^\.]\b)'+na[0]+r'\b', na[1], newBody)
        script = script.replace(oldBody, newBody)
    # delete the docstring
    for v in functions.values():
        if v["doc"] is not None:
            script = re.sub(r'( )*'+v["doc"], '', script)
    # avoid __method__
    for k in functions.keys():
        if not k.startswith('__'):
            script = re.sub(r'\b'+k+r'\b', next(randGen), script)
    return script

def get_classes(script):
    classes = {}
    return re.findall(r'\bclass (\w+)\(.*\):\n', script)

def main(script):
    """
    Keep order
    if join_function_call before one_line:
        if x:
            fcall()    =X>   if x: fcall(); fcall2()
        fcall2()
    """
    global randGen
    randGen = rand_name_gen2(script)
    script = purge_spaces(script)
    script = delete_comments(script)
    #script = replace_global_var(script) ne pas utiliser !!!
    script = purge_spaces(script)
    script = replace_functions(script)
    script = one_line(script)
    script = join_similar_line(script)
    return script

if __name__ == '__main__':
    path = "modele.py"
    script = get_script(path)
    script = main(script)
    write_script(path, purge_spaces(script))

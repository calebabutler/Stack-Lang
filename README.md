# Stack-Lang
A simple stack based language with lists as its only data structure. Requires python.

# Primitives
The language is only defined with functions. By default, there are only 3 data types, numbers, symbols and lists.
Here are the built-in functions.

    dup         ; duplicates what is on top of the stack
    exch        ; flips the top two items on the stack
    pop         ; pops off the top item of the stack
    stack->list ; converts the stack to a list and adds the list to the top of the stack
    
    +           ; add top 2 numbers on the stack
    -           ; subtract top 2 numbers on the stack
    *           ; multiply top 2 numbers on the stack
    /           ; divide top 2 numbers on the stack
    %           ; modulus of the top 2 numbers on the stack
    floor       ; floor of the top 2 numbers on the stack
    
    =           ; adds 't' or 'f' depending on if two things are equal or not
    <           ; finds if two numbers are less than, adds 't' or 'f'
    >           ; finds if two numbers are greater than, adds 't' or 'f'

    type        ; gives type of the top of the stack, 'list', 'number' or 'symbol'
    first       ; first item of list/symbol
    rest        ; rest of a list/symbol
    pair        ; pairing two lists, same as cons in lisp
    concat      ; pairs two symbols or lists of any type
    print       ; prints top of stack
    
    if          ; gets third value off stack, if 't' executes 2nd stack list, if 'f' executes top stack list
    !           ; executes list on top of the stack
    def         ; takes in a symbol (quoted with '), and a value that it represents.
    popdef      ; pops the last definition off of the definitions stack
    defun       ; takes in a symbol (quoted with '), and a list executed on runtime.
    popfun      ; pops the last function definition off of the functions stack

if your command isn't a primitive, it will either run a predefined function/value or it will be added to the stack as a symbol/number. Lists are written like this:

    (1 2 3 4)

everything is in postfix notation. Also, everything is stack based.

    (1 2 3 4)
        stack = [[1, 2, 3, 4]]
    first
        stack = [1]
    4
        stack = [1, 4]
    +
        stack = [5]
    print
        5
        stack = []
    
    (1 2 3 4) first 4 + print ; same code, written on one line

even functions are defined in a stack based way:

    'factorial (dup 0 = (pop 1) (dup 1 - factorial *) if) defun

    5 factorial print ; -> 120

notice the difference between functions and values. Functions are just lists that are ran at run time. This can easily be rewritten as:


    'factorial (dup 0 = (pop 1) (dup 1 - factorial *) if) def
    
    5 factorial ! print ; -> also 120
    
    factorial print ; -> (dup 0 = (pop 1) (dup 1 - factorial *) if) not error

theoretically, there is no need for lambdas because functions have no arguments. So, in a theoretical situation, a map function would look like:

    (1 2 3 4) (3 +) map ; -> (4 5 6 7)

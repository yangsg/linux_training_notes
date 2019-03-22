# [Defining Functions](https://docs.python.org/3.6/tutorial/controlflow.html#defining-functions)

> The execution of a function introduces a new symbol table used for the local
> variables of the function. More precisely, all variable assignments in
> a function store the value in the local symbol table; whereas variable
> references first look in the local symbol table, then in the local symbol
> tables of enclosing functions, then in the global symbol table, and finally in
> the table of built-in names. Thus, global variables cannot be directly assigned
> a value within a function (unless named in a global statement), although they
> may be referenced.


> The actual parameters (arguments) to a function call are introduced in the
> local symbol table of the called function when it is called; thus, arguments
> are passed using call by value (where the value is always an object reference,
> not the value of the object). [1] When a function calls another function, a new
> local symbol table is created for that call.


函数没有return语句，则默认返回None, 
查看None可通过语句： print(None)




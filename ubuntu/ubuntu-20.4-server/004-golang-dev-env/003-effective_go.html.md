
- [Effective Go](https://golang.google.cn/doc/effective_go.html#introduction)


### gofmt:源码格式化工具
```go
type T struct {
    name    string // name of the object
    value   int    // its value
}
```

小节:
- go 默认使用 tab 缩进, 
- line 没有长度限制
- 仅需更少的括号"()" //如在 if for switch 语句中


### 注释:Commentary

```go
/* C-style block comments */
// C++-style line comments
```

- godoc 用于 提取相关 comment
- 每个 package 都应该有 a package comment, a block comment preceding the package clause. 对于由多文件组成的包，package comment 仅需在 one file 文件中被提供


### 名称:Names


- name 的首字母大小写还与该 name 的可见性有关

#### 包名:Package names
 

```go

//导入一个package 时，该 package name 就成了该 package 内容的的一个访问器(an accessor)
import "bytes"
```

- package name should be good: short, concise, evocative. By convention, packages are given lower case, single-word names; 
// package name 为 被 imports 的默认 name

-  另一个约定： package name 是其 source directory 的 base name; 如 src/encoding/base64 通过 "encoding/base64" 被导入，且其 name 为 base64, 不要写成 encoding_base64 或 encodingBase64. */

- Similarly, the function to make new instances of ring.Ring—which is the definition of a constructor in Go—would normally be called NewRing, but since Ring is the only type exported by the package, and since the package is called ring, it's called just New, which clients of the package see as ring.New. Use the package structure to help you choose good names.
// 利用 package structure 来选择 good names.


#### Getters: getter 方法命名约定

- go 语言中通常 getters 和 setters 都是不需要的。非要使用的场合，可以使用:
```go

/*
  如针对 unexported 的 owner 字段的 
  getter 方法，命名为 Owner，
  其 setter 方法命名为 SetOwner
*/
owner := obj.Owner()
if owner != user {
    obj.SetOwner(user)
}
```

#### Interface names: 接口名

- By convention, one-method interfaces are named by the method name plus an -er suffix or similar modification to construct an agent noun: Reader, Writer, Formatter, CloseNotifier etc.

- 许多 names 如 Read, Write, Close, Flush, String 等等具有 权威的 signatures 和 meanings，通常应该避免使用它们来命名你的 method, 非常这些 method 具有相同的 meanings.

#### MixedCaps
- go 中约定使用 MixedCaps 和 mixedCaps 而非 underscores 来书写 multiword names.


#### Semicolons:分号
- 类似于 C 语言，go 使用 semicolons 来 terminate statements。但多数时候 分号 都不是必须的, lexer(词法分析程序) 会使用 a simple rule 来自动的插入分号 
```go
/*
  如下 开括号 “{” 必须与 "if i < f()" 在同一行上。
  否则 semicolon insertion rules 会导致错误。
*/
if i < f() {
    g()
}
```


### Control structures：控制结构

- go 没有 do 和 while 循环， 仅有一个简单通用的 for
- switch 更加灵活，if 和 switch 和 for 一样，都可 可选择的接收一个 initialization statement。
- break 和 continue 都可以 可选择的 接收一个 label.
-  a type switch and a multiway communications multiplexer, select.


#### if

```go
if x > 0 {
    return y
}
```

- 示例: 一个接收 可选的 initialization statement 的语句
```go
// 该示例新建了一个 名为 err 的 a local variable
if err := file.Chmod(0664); err != nil {
    log.Print(err)
    return err
}
```

```go
f, err := os.Open(name)
if err != nil {
    return err
}
codeUsing(f)
```

```go
f, err := os.Open(name)
if err != nil {
    return err
}
d, err := f.Stat()
if err != nil {
    f.Close()
    return err
}
codeUsing(f, d)
```

#### Redeclaration and reassignment:重复声明和重复赋值
- := 一种简写形式的声明

```go
f, err := os.Open(name) //声明了 2 个变量: f, err
if err != nil {
    return err
}
d, err := f.Stat() //对 err 重新赋值，声明了 d
if err != nil {
    f.Close()
    return err
}
codeUsing(f, d)
```

- § It's worth noting here that in Go the scope of function parameters and return values is the same as the function body, even though they appear lexically outside the braces that enclose the body.

#### For

- go 中的 for loop 同一了 for 和 while, 且 go 没有  do-while. 有 3 中形式的 for 循环:
```go
// Like a C for
for init; condition; post { }

// Like a C while
for condition { }

// Like a C for(;;)
for { }
```

- Short declarations make it easy to declare the index variable right in the loop.
```go
sum := 0
for i := 0; i < 10; i++ { // := 便于声明 loop 使用的  index 变量
    sum += i
}
```

- If you're looping over an array, slice, string, or map, or reading from a channel, a range clause can manage the loop.

```go
// 可以使用 range 子句来 遍历 array, slice, string, map 或读取 channel
for key, value := range oldMap {
    newMap[key] = value
}
```

- If you only need the first item in the range (the key or index), drop the second:
```go
// 如果仅需 range 中第一个 item(如 key 或 index), 丢弃 第二个即可
for key := range m {
    if key.expired() {
        delete(m, key)
    }
}
```

- If you only need the second item in the range (the value), use the blank identifier, an underscore, to discard the first:

```go
sum := 0
for _, value := range array { //使用空白标识符 _ 丢弃第一个 item(如 key 或 index)
    sum += value
}
```

- 空白标识符 _ 的更多用法见 [blank](https://golang.google.cn/doc/effective_go.html#blank)




- For strings, the range does more work for you, breaking out individual Unicode code points by parsing the UTF-8. Erroneous encodings consume one byte and produce the replacement rune U+FFFD.
> 对于 strings， range 做了更多的工作: 通过解析 UTF-8 分离出 单个的 Unicode code points. 错误的编码(Erroneous encodings) 会消耗 one byte 并生成 替代的 rune U+FFFD.  更多rune(符文) 的信息见 [rune](https://golang.google.cn/ref/spec#Rune_literals)


```go
for pos, char := range "日本\x80語" { // \x80 is an illegal UTF-8 encoding
    fmt.Printf("character %#U starts at byte position %d\n", char, pos)
}
```

```log
character U+65E5 '日' starts at byte position 0
character U+672C '本' starts at byte position 3
character U+FFFD '�' starts at byte position 6
character U+8A9E '語' starts at byte position 7
```


- Finally, Go has no comma operator and ++ and -- are statements not expressions. Thus if you want to run multiple variables in a for you should use parallel assignment (although that precludes ++ and --).
> go 没有逗号操作符 且 ++ 和 -- 是语句 而非表达式。因此当想要在 for 循环中使用 multiple variables，则应该使用 并行赋值(parallel assignment)


#### Switch

- go 的 switch 比 c 语言中的 更通用，其 expressions 不必非得是 constants or even integers, if the switch has no expression it switches on true. It's therefore possible—and idiomatic—to write an if-else-if-else chain as a switch.

```go
func unhex(c byte) byte {
    switch {
    case '0' <= c && c <= '9':
        return c - '0'
    case 'a' <= c && c <= 'f':
        return c - 'a' + 10
    case 'A' <= c && c <= 'F':
        return c - 'A' + 10
    }
    return 0
}
```

- There is no automatic fall through, but cases can be presented in comma-separated lists.
> go 的 switch 中没有自动的 fall through.

```go
func shouldEscape(c byte) bool {
    switch c {
    case ' ', '?', '&', '=', '#', '+', '%':
        return true
    }
    return false
}
```

- 带 label 的 break 语句 可用于跳出包围它的 loop
```go
Loop:
	for n := 0; n < len(src); n += size {
		switch {
		case src[n] < sizeOne:
			if validateOnly {
				break
			}
			size = 1
			update(src[n])

		case src[n] < sizeTwo:
			if n+1 >= len(src) {
				err = errShortInput
				break Loop
			}
			if validateOnly {
				break
			}
			size = 2
			update(src[n] + src[n+1]<<shift)
		}
	}
```

- continue 语句也可以接收可选的 label，当其仅用于 loops.


```go
// Compare returns an integer comparing the two byte slices,
// lexicographically.
// The result will be 0 if a == b, -1 if a < b, and +1 if a > b
func Compare(a, b []byte) int {
    for i := 0; i < len(a) && i < len(b); i++ {
        switch {
        case a[i] > b[i]:
            return 1
        case a[i] < b[i]:
            return -1
        }
    }
    switch {
    case len(a) > len(b):
        return 1
    case len(a) < len(b):
        return -1
    }
    return 0
}
```

#### Type switch

> switch 还可用于 发现 an interface 的 dynamic type。Such a type switch uses the syntax of a type assertion with the keyword type inside the parentheses. If the switch declares a variable in the expression, the variable will have the corresponding type in each clause. It's also idiomatic to reuse the name in such cases, in effect declaring a new variable with the same name but a different type in each case.

```go
var t interface{}
t = functionOfSomeType()
switch t := t.(type) {
default:
    fmt.Printf("unexpected type %T\n", t)     // %T prints whatever type t has
case bool:
    fmt.Printf("boolean %t\n", t)             // t has type bool
case int:
    fmt.Printf("integer %d\n", t)             // t has type int
case *bool:
    fmt.Printf("pointer to boolean %t\n", *t) // t has type *bool
case *int:
    fmt.Printf("pointer to integer %d\n", *t) // t has type *int
}
```

### Functions：函数

#### Multiple return values

- go 中 functions 和 methods 可以 return multiple values. 这种形式 可以改善 C 语言程序中 2 个笨拙的习惯用法：in-band error returns such as -1 for EOF and modifying an argument passed by address.

```go
// package os 

/*
 it returns the number of bytes written and a non-nil error when n != len(b).
*/
func (file *File) Write(b []byte) (n int, err error)
```

```go
func nextInt(b []byte, i int) (int, int) {
    for ; i < len(b) && !isDigit(b[i]); i++ {
    }
    x := 0
    for ; i < len(b) && isDigit(b[i]); i++ {
        x = x*10 + int(b[i]) - '0'
    }
    return x, i
}
```
```go
    for i := 0; i < len(b); {
        x, i = nextInt(b, i)
        fmt.Println(x)
    }
```

#### Named result parameters

- The return or result "parameters" of a Go function can be given names and used as regular variables, just like the incoming parameters. When named, they are initialized to the zero values for their types when the function begins; if the function executes a return statement with no arguments, the current values of the result parameters are used as the returned values.

```go
func nextInt(b []byte, pos int) (value, nextPos int) {
```

```go
func ReadFull(r Reader, buf []byte) (n int, err error) {
    for len(buf) > 0 && err == nil {
        var nr int
        nr, err = r.Read(buf)
        n += nr
        buf = buf[nr:]
    }
    return
}
```


### Defer

- defer 语句计划 the deferred function  在 该 defer 语句 所在的 function 执行 return 之前 被调用。 It's an unusual but effective way to deal with situations such as resources that must be released regardless of which path a function takes to return. The canonical examples are unlocking a mutex or closing a file.
```go
// Contents returns the file's contents as a string.
func Contents(filename string) (string, error) {
    f, err := os.Open(filename)
    if err != nil {
        return "", err
    }
    defer f.Close()  // f.Close will run when we're finished.

    var result []byte
    buf := make([]byte, 100)
    for {
        n, err := f.Read(buf[0:])
        result = append(result, buf[0:n]...) // append is discussed later.
        if err != nil {
            if err == io.EOF {
                break
            }
            return "", err  // f will be closed if we return here.
        }
    }
    return string(result), nil // f will be closed if we return here.
}
```

- defer 类似 Close 的两个优点:1. 保证能被执行; 2. 将其置于 Open 的地方，代码更清晰


- The arguments to the deferred function (which include the receiver if the function is a method) are evaluated when the defer executes, not when the call executes. Besides avoiding worries about variables changing values as the function executes, this means that a single deferred call site can defer multiple function executions. Here's a silly example.
> deferred function 的 实参(如果是 methods, 还包括其 receiver) 是在 defer statement 被执行时求得的，而非是在 the deferred function 被执行的时候求得的。

```go
for i := 0; i < 5; i++ {
    defer fmt.Printf("%d ", i)
}

//output: 4 3 2 1 0
```

- Deferred functions are executed in LIFO order, so this code will cause 4 3 2 1 0 to be printed when the function returns. A more plausible example is a simple way to trace function execution through the program. We could write a couple of simple tracing routines like this:
> Deferred functions 的按 LIFO(last in first out) 的顺序执行。//注: 其实这就是有一种 栈(stack) 的 出栈和入栈相同

```go
func trace(s string)   { fmt.Println("entering:", s) }
func untrace(s string) { fmt.Println("leaving:", s) }

// Use them like this:
func a() {
    trace("a")
    defer untrace("a")
    // do something....
}
```

- We can do better by exploiting the fact that arguments to deferred functions are evaluated when the defer executes. The tracing routine can set up the argument to the untracing routine. This example:
```go
func trace(s string) string {
    fmt.Println("entering:", s)
    return s
}

func un(s string) {
    fmt.Println("leaving:", s)
}

func a() {
    defer un(trace("a"))
    fmt.Println("in a")
}

func b() {
    defer un(trace("b"))
    fmt.Println("in b")
    a()
}

func main() {
    b()
}
```

prints
```log
entering: b
in b
entering: a
in a
leaving: a
leaving: b
```


### Data: 数据

#### Allocation with new：使用 new 分配

- Go has two allocation primitives, the built-in functions new and make. They do different things and apply to different types, which can be confusing, but the rules are simple. Let's talk about new first. It's a built-in function that allocates memory, but unlike its namesakes in some other languages it does not initialize the memory, it only zeros it. That is, new(T) allocates zeroed storage for a new item of type T and returns its address, a value of type *T. In Go terminology, it returns a pointer to a newly allocated zero value of type T.
> Go 具有 2 个 分配原语， 即 new 和 make 这 2 个内置函数。
> 函数 new 并不会初始化内存， 它仅将其 置为 0. 也就是说，new(T) 为 T 类型的新项 分配 被置 0 的存储 并 返回其 address, 其 类型为 *T. 在 Go 术语中， 它返回的是一个 指向被新分配的 T 类型的 zero value 的指针。

- Since the memory returned by new is zeroed, it's helpful to arrange when designing your data structures that the zero value of each type can be used without further initialization. This means a user of the data structure can create one with new and get right to work. For example, the documentation for bytes.Buffer states that "the zero value for Buffer is an empty buffer ready to use." Similarly, sync.Mutex does not have an explicit constructor or Init method. Instead, the zero value for a sync.Mutex is defined to be an unlocked mutex.
> 因为 有 内置函数 new 返回的 memory 被置为 0, 当在 设计 其 每个 type 的 zero value 就可以使用 而无需更多初始化的数据结构的时候这种安排是很有用的。

The zero-value-is-useful property works transitively. Consider this type declaration.

```go
type SyncedBuffer struct {
    lock    sync.Mutex //注: sync.Mutex 的 zero value 被定义为一个 unlocked mutex.
    buffer  bytes.Buffer //注: zero value 对于 Buffer 意味着 一个准备被使用的 empty buffer.
}
```

Values of type SyncedBuffer are also ready to use immediately upon allocation or just declaration. In the next snippet, both p and v will work correctly without further arrangement.

```go
p := new(SyncedBuffer)  // type *SyncedBuffer
var v SyncedBuffer      // type  SyncedBuffer
```

#### Constructors and composite literals

- Sometimes the zero value isn't good enough and an initializing constructor is necessary, as in this example derived from package os.
> 有时 zero value 还不足够 且还需要一个初始化构造器。

```go
func NewFile(fd int, name string) *File {
    if fd < 0 {
        return nil
    }
    f := new(File)
    f.fd = fd
    f.name = name
    f.dirinfo = nil
    f.nepipe = 0
    return f
}
```

- There's a lot of boiler plate in there. We can simplify it using a composite literal, which is an expression that creates a new instance each time it is evaluated.
> 复合字面量(composite literal), 其是一个 表达式(expression), 每次它被求值时都会创建一个新实例(a new instance)

```go
func NewFile(fd int, name string) *File {
    if fd < 0 {
        return nil
    }
    f := File{fd, name, nil, 0}
    return &f
}
```

- Note that, unlike in C, it's perfectly OK to return the address of a local variable; the storage associated with the variable survives after the function returns. In fact, taking the address of a composite literal allocates a fresh instance each time it is evaluated, so we can combine these last two lines.
> 注: 与 C 语言不同， 返回 a local variable 的 address 是完全 OK 的；与 该 variable 所关联的 存储区(storage) 在其 function returns 后仍 存活下来。

```go
    return &File{fd, name, nil, 0}
```

The fields of a composite literal are laid out in order and must all be present. However, by labeling the elements explicitly as field:value pairs, the initializers can appear in any order, with the missing ones left as their respective zero values. Thus we could say
```go
// 带标签(即字段名) 的 a composite literal
    return &File{fd: fd, name: name}
```

As a limiting case, if a composite literal contains no fields at all, it creates a zero value for the type. The expressions new(File) and &File{} are equivalent.


Composite literals can also be created for arrays, slices, and maps, with the field labels being indices or map keys as appropriate. In these examples, the initializations work regardless of the values of Enone, Eio, and Einval, as long as they are distinct.
> 复合字面量 还可用于创建 arrays, slices 和 maps.
```go
a := [...]string   {Enone: "no error", Eio: "Eio", Einval: "invalid argument"}
s := []string      {Enone: "no error", Eio: "Eio", Einval: "invalid argument"}
m := map[int]string{Enone: "no error", Eio: "Eio", Einval: "invalid argument"}
```

```go
package main

import "fmt"

func main() {
        const Enone = 1
        const   Eio = 0
        const Einval = 2

        a := [...]string   {Enone: "no error", Eio: "Eio", Einval: "invalid argument"}
        s := []string      {Enone: "no error", Eio: "Eio", Einval: "invalid argument"}
        m := map[int]string{Enone: "no error", Eio: "Eio", Einval: "invalid argument"}

  fmt.Printf("%v\n", a)
  fmt.Printf("%v\n", s)
  fmt.Printf("%v\n", m)

/*
output:
[Eio no error invalid argument]
[Eio no error invalid argument]
map[0:Eio 1:no error 2:invalid argument]

*/
}

```



#### Allocation with make

- Back to allocation. The built-in function make(T, args) serves a purpose different from new(T). It creates slices, maps, and channels only, and it returns an initialized (not zeroed) value of type T (not *T). The reason for the distinction is that these three types represent, under the covers, references to data structures that must be initialized before use. A slice, for example, is a three-item descriptor containing a pointer to the data (inside an array), the length, and the capacity, and until those items are initialized, the slice is nil. For slices, maps, and channels, make initializes the internal data structure and prepares the value for use. For instance,
> make(T, args) 与 new(T) 的目标不同，make(T, args) 仅用于创建 slices, maps, 和 channels，其 returns 类型T(非 *T) 的被初始化过(非 zeroed)的 value. 这种区别是因为 这 3 中类型的底层表示中引用了 在使用之前 必须被初始化的 data structures. 例如 a slice, 就是 一个底层 包含 3 个 item 的 描述符(descriptor). 其包含了 指向 data(在 an array 中) 的 pointer(指针), length(长度) 和 capacity(容量), 且直到 这 3 项被初始化之前，slice 都为 nil. 对于 slices, maps, and channels, make 会为其 初始化 内部的 data structure 并 准备 value 以便使用

```go
make([]int, 10, 100)
```

-  new([]int) returns a pointer to a newly allocated, zeroed slice structure, that is, a pointer to a nil slice value.

```go
package main

import "fmt"

func main() {
  p1 := new([]int)

  fmt.Printf("%s\n","new([]int))")
  fmt.Printf("\t%v\n", p1)
  fmt.Printf("\t%T\n", p1)
  p2 := &[]int{10, 20, 30}
  fmt.Printf("%s\n","&[]int{10, 20, 30}")
  fmt.Printf("\t%v\n", p2)
  fmt.Printf("\t%T\n", p2)
}

/*
output:
new([]int))
        &[]
        *[]int
&[]int{10, 20, 30}
        &[10 20 30]
        *[]int
*/
```

- These examples illustrate the difference between new and make.
```go
var p *[]int = new([]int)       // allocates slice structure; *p == nil; rarely useful
var v  []int = make([]int, 100) // the slice v now refers to a new array of 100 ints

// Unnecessarily complex:
var p *[]int = new([]int)
*p = make([]int, 100, 100)

// Idiomatic:
v := make([]int, 100)
```

- Remember that make applies only to maps, slices and channels and does not return a pointer. To obtain an explicit pointer allocate with new or take the address of a variable explicitly.
> 记住： make 仅应用于  maps, slices and channels 且其 不会 return a pointer. 为了 获取 一个 显示的 指针，可以使用 new 来分配 或 显示地 获取 a variable 的 address.


#### Arrays
- Arrays are useful when planning the detailed layout of memory and sometimes can help avoid allocation, but primarily they are a building block for slices, the subject of the next section. To lay the foundation for that topic, here are a few words about arrays.
> Arrays 是 slices 底层的一个 a building block.

- There are major differences between the ways arrays work in Go and C. In Go,
> Go 中 arrays 的工作方式 与其在 C 语言中的工作方式的区别:

1. Arrays are values. Assigning one array to another copies all the elements.
> Arrays 是 values(值类型)。 将 一个 array 赋值给 另一个 array 会 拷贝 所有的 elements.
2. In particular, if you pass an array to a function, it will receive a copy of the array, not a pointer to it.
> 特别地，如果将 an array 传递给 a function, 该 function 则会 接收  该 array 的一份 拷贝(copy), 而不是 指向该 array 的 a pointer.
3. The size of an array is part of its type. The types [10]int and [20]int are distinct.
> an array 的 size 是该 数组类型的一部分。所以 类型 [10]int 和 [20]int 是不同的。


The value property can be useful but also expensive; if you want C-like behavior and efficiency, you can pass a pointer to the array.
> array 的这种总 value 特性 可能很有用但是 开销也比较昂贵； 所有如果需要 类似 C 语言中 数组的 行为和效率，则可以传递指向 array 的 a pointer.
```go
func Sum(a *[3]float64) (sum float64) {
    for _, v := range *a {
        sum += v
    }
    return
}

array := [...]float64{7.0, 8.5, 9.1}
x := Sum(&array)  // Note the explicit address-of operator
```
> 注: 但是 这并非 Go 的惯用法，此时应该使用 idiomatic；

#### Slices

Slices wrap arrays to give a more general, powerful, and convenient interface to sequences of data. Except for items with explicit dimension such as transformation matrices, most array programming in Go is done with slices rather than simple arrays.
> Slices 是对 arrays 的封装，其提供了 资格 data 序列的 更通用(general), 强大(powerful) 和 方便(convenient) 的 接口(interface).除了具有显式维数的项（如转换矩阵）之外，Go中的大多数数组编程都是用 slices 而不是简单的 arrays 来完成的。


Slices hold references to an underlying array, and if you assign one slice to another, both refer to the same array. If a function takes a slice argument, changes it makes to the elements of the slice will be visible to the caller, analogous to passing a pointer to the underlying array. A Read function can therefore accept a slice argument rather than a pointer and a count; the length within the slice sets an upper limit of how much data to read. Here is the signature of the Read method of the File type in package os:
>  Slices 持有 一个其 底层 array 的 引用(references), 且 如果 将 一个 slice 赋值给 另一个 slice, 则这 2 个 slice 的 references 都引用 同一个 array. 如果 a function 接收一个 slice 实参，则对该 slice 的 elements 的修改 也将对 caller 可见，类似于传递 一个 指向 the underlying array 的 a pointer.
```go
func (f *File) Read(buf []byte) (n int, err error)
```

The method returns the number of bytes read and an error value, if any. To read into the first 32 bytes of a larger buffer buf, slice (here used as a verb) the buffer.

```go
    n, err := f.Read(buf[0:32])
```

Such slicing is common and efficient. In fact, leaving efficiency aside for the moment, the following snippet would also read the first 32 bytes of the buffer.

```go
    var n int
    var err error
    for i := 0; i < 32; i++ {
        nbytes, e := f.Read(buf[i:i+1])  // Read one byte.
        n += nbytes
        if nbytes == 0 || e != nil {
            err = e
            break
        }
    }
```

The length of a slice may be changed as long as it still fits within the limits of the underlying array; just assign it to a slice of itself. The capacity of a slice, accessible by the built-in function cap, reports the maximum length the slice may assume. Here is a function to append data to a slice. If the data exceeds the capacity, the slice is reallocated. The resulting slice is returned. The function uses the fact that len and cap are legal when applied to the nil slice, and return 0.

```go
//注: 内置函数 len 可获取 slice 中 elements 的 个数(即 slice 的 length), 函数 cap 获取 当前 slice 的 capacity(当前最大容量).
func Append(slice, data []byte) []byte {
    l := len(slice)
    if l + len(data) > cap(slice) {  // reallocate
        // Allocate double what's needed, for future growth.
        newSlice := make([]byte, (l+len(data))*2)
        // The copy function is predeclared and works for any slice type.
        copy(newSlice, slice)
        slice = newSlice
    }
    slice = slice[0:l+len(data)]
    copy(slice[l:], data)
    return slice
}
```

We must return the slice afterwards because, although Append can modify the elements of slice, the slice itself (the run-time data structure holding the pointer, length, and capacity) is passed by value.
> 然后我们必须 return 该 slice, 尽管 函数 Append 可以修改 slice 的 elements, 但是 slice 自己本身(其运行时的数据结构持有 the pointer, length, 和 capacity ) 是 通过 值传递的。


The idea of appending to a slice is so useful it's captured by the append built-in function. To understand that function's design, though, we need a little more information, so we'll return to it later.


#### Two-dimensional slices : 二维 slices

Go's arrays and slices are one-dimensional. To create the equivalent of a 2D array or slice, it is necessary to define an array-of-arrays or slice-of-slices, like this:

```go
type Transform [3][3]float64  // A 3x3 array, really an array of arrays.
type LinesOfText [][]byte     // A slice of byte slices.
```

Because slices are variable-length, it is possible to have each inner slice be a different length. That can be a common situation, as in our LinesOfText example: each line has an independent length.

```go
text := LinesOfText{
	[]byte("Now is the time"),
	[]byte("for all good gophers"),
	[]byte("to bring some fun to the party."),
}
```

Sometimes it's necessary to allocate a 2D slice, a situation that can arise when processing scan lines of pixels, for instance. There are two ways to achieve this. One is to allocate each slice independently; the other is to allocate a single array and point the individual slices into it. Which to use depends on your application. If the slices might grow or shrink, they should be allocated independently to avoid overwriting the next line; if not, it can be more efficient to construct the object with a single allocation. For reference, here are sketches of the two methods. First, a line at a time:
> 分配 2 维 slice
```go
// Allocate the top-level slice.
picture := make([][]uint8, YSize) // One row per unit of y.
// Loop over the rows, allocating the slice for each row.
for i := range picture {
	picture[i] = make([]uint8, XSize)
}
```

And now as one allocation, sliced into lines:

```go
// Allocate the top-level slice, the same as before.
picture := make([][]uint8, YSize) // One row per unit of y.
// Allocate one large slice to hold all the pixels.
pixels := make([]uint8, XSize*YSize) // Has type []uint8 even though picture is [][]uint8.
// Loop over the rows, slicing each row from the front of the remaining pixels slice.
for i := range picture {
	picture[i], pixels = pixels[:XSize], pixels[XSize:]
}
```

#### Maps

Maps are a convenient and powerful built-in data structure that associate values of one type (the key) with values of another type (the element or value). The key can be of any type for which the equality operator is defined, such as integers, floating point and complex numbers, strings, pointers, interfaces (as long as the dynamic type supports equality), structs and arrays. Slices cannot be used as map keys, because equality is not defined on them. Like slices, maps hold references to an underlying data structure. If you pass a map to a function that changes the contents of the map, the changes will be visible in the caller.

> Maps 是一张 关联 key 和 value 的 内置的 数据结构，key 可以是 其 equality operator 被定义了的任意的类型(any type), 例如  integers, floating point and complex numbers, strings, pointers, interfaces (as long as the dynamic type supports equality), structs and arrays.
> 注: Slices 不能作为 map 的 key, 因为其上没有定义 equality.
> 与 slices 类似，maps 持有一个 指向 底层 data structure 的引用(references). 如果将 a map 传递给 a function, 而 该 function 又会修改 该 map 的内容，则 该修改 在 caller 中是 可见的。

Assigning and fetching map values looks syntactically just like doing the same for arrays and slices except that the index doesn't need to be an integer.

```go
offset := timeZone["EST"]
```

An attempt to fetch a map value with a key that is not present in the map will return the zero value for the type of the entries in the map. For instance, if the map contains integers, looking up a non-existent key will return 0. A set can be implemented as a map with value type bool. Set the map entry to true to put the value in the set, and then test it by simple indexing.
> 试图使用一个 在 map 中不存在的 key 获取对应的 value 将返回 zero value.
```go
// 利用 其 value 类型为 bool 的 map 可以实现 集合类型(set)
attended := map[string]bool{
    "Ann": true,
    "Joe": true,
    ...
}

if attended[person] { // will be false if person is not in the map
    fmt.Println(person, "was at the meeting")
}
```

Sometimes you need to distinguish a missing entry from a zero value. Is there an entry for "UTC" or is that 0 because it's not in the map at all? You can discriminate with a form of multiple assignment.

```go
// 可以使用 多赋值 可以区分 map 中 value 为 zero value 和 key 不存在的情况 
var seconds int
var ok bool
seconds, ok = timeZone[tz]
```



For obvious reasons this is called the “comma ok” idiom. In this example, if tz is present, seconds will be set appropriately and ok will be true; if not, seconds will be set to zero and ok will be false. Here's a function that puts it together with a nice error report:

```go
func offset(tz string) int {
    //注: 带额外的 ok 变量的这种方式被称为 “comma ok” 惯用法
    if seconds, ok := timeZone[tz]; ok {
        return seconds
    }
    log.Println("unknown time zone:", tz)
    return 0
}
```

To test for presence in the map without worrying about the actual value, you can use the blank identifier (_) in place of the usual variable for the value.

```go
// 仅测试 存在性是 可以利用空白运算符 _ 忽略 value 的赋值。
_, present := timeZone[tz]
```


To delete a map entry, use the delete built-in function, whose arguments are the map and the key to be deleted. It's safe to do this even if the key is already absent from the map.

```go
// 可以使用 内置函数 delete 从 map 中 删除某一项, 该 delete 操作即使其 key 并不存在于 map 中时也是安全的。
delete(timeZone, "PDT")  // Now on Standard Time
```

#### Printing

Formatted printing in Go uses a style similar to C's printf family but is richer and more general. The functions live in the fmt package and have capitalized names: fmt.Printf, fmt.Fprintf, fmt.Sprintf and so on. The string functions (Sprintf etc.) return a string rather than filling in a provided buffer.

> Go 中的 格式化打印 使用与 C 语言中 printf 家族 类似的风格，但是其更 丰富 和 更通用。 这些函数 存在于 fmt 包中，有 fmt.Printf, fmt.Fprintf, fmt.Sprintf 等。而 string functions(Sprintf etc.) 返回 a string 而非 填充进 一个提供的 buffer 中。



You don't need to provide a format string. For each of Printf, Fprintf and Sprintf there is another pair of functions, for instance Print and Println. These functions do not take a format string but instead generate a default format for each argument. The Println versions also insert a blank between arguments and append a newline to the output while the Print versions add blanks only if the operand on neither side is a string. In this example each line produces the same output.

```go
fmt.Printf("Hello %d\n", 23)
fmt.Fprint(os.Stdout, "Hello ", 23, "\n")
fmt.Println("Hello", 23)
fmt.Println(fmt.Sprint("Hello ", 23))
```


The formatted print functions fmt.Fprint and friends take as a first argument any object that implements the io.Writer interface; the variables os.Stdout and os.Stderr are familiar instances.


Here things start to diverge from C. First, the numeric formats such as %d do not take flags for signedness or size; instead, the printing routines use the type of the argument to decide these properties.

```go
var x uint64 = 1<<64 - 1
fmt.Printf("%d %x; %d %x\n", x, x, int64(x), int64(x))

//output: 18446744073709551615 ffffffffffffffff; -1 -1
```


If you just want the default conversion, such as decimal for integers, you can use the catchall format %v (for “value”); the result is exactly what Print and Println would produce. Moreover, that format can print any value, even arrays, slices, structs, and maps. Here is a print statement for the time zone map defined in the previous section.
```go
fmt.Printf("%v\n", timeZone)  // or just fmt.Println(timeZone)

//output: map[CST:-21600 EST:-18000 MST:-25200 PST:-28800 UTC:0]
```

For maps, Printf and friends sort the output lexicographically by key.

When printing a struct, the modified format %+v annotates the fields of the structure with their names, and for any value the alternate format %#v prints the value in full Go syntax.

```go
type T struct {
    a int
    b float64
    c string
}
t := &T{ 7, -2.35, "abc\tdef" }
fmt.Printf("%v\n", t)
fmt.Printf("%+v\n", t) //output: &{a:7 b:-2.35 c:abc     def}
fmt.Printf("%#v\n", t) //&main.T{a:7, b:-2.35, c:"abc\tdef"}
fmt.Printf("%#v\n", timeZone)
```

```log
&{7 -2.35 abc   def}
&{a:7 b:-2.35 c:abc     def}
&main.T{a:7, b:-2.35, c:"abc\tdef"}
map[string]int{"CST":-21600, "EST":-18000, "MST":-25200, "PST":-28800, "UTC":0}
```

(Note the ampersands.) That quoted string format is also available through %q when applied to a value of type string or []byte. The alternate format %#q will use backquotes instead if possible. (The %q format also applies to integers and runes, producing a single-quoted rune constant.) Also, %x works on strings, byte arrays and byte slices as well as on integers, generating a long hexadecimal string, and with a space in the format (% x) it puts spaces between the bytes.
```go

package main

import "fmt"

func main() {
        //利用 %q 输出 quoted string
        fmt.Printf("%q\n", "hello") //output: "hello"
        fmt.Printf("%q\n", []byte{65, 66}) //output: "AB"
}


```


Another handy format is %T, which prints the type of a value.
```go
fmt.Printf("%T\n", timeZone)  //打印类型,  map[string]int
```

If you want to control the default format for a custom type, all that's required is to define a method with the signature String() string on the type. For our simple type T, that might look like this.
```go
func (t *T) String() string {
    return fmt.Sprintf("%d/%g/%q", t.a, t.b, t.c)
}
fmt.Printf("%v\n", t)
```
to print in the format
```log
7/-2.35/"abc\tdef"
```

(If you need to print values of type T as well as pointers to T, the receiver for String must be of value type; this example used a pointer because that's more efficient and idiomatic for struct types. See the section below on pointers vs. value receivers for more information.)


Our String method is able to call Sprintf because the print routines are fully reentrant and can be wrapped this way. There is one important detail to understand about this approach, however: don't construct a String method by calling Sprintf in a way that will recur into your String method indefinitely. This can happen if the Sprintf call attempts to print the receiver directly as a string, which in turn will invoke the method again. It's a common and easy mistake to make, as this example shows.

```go
type MyString string

func (m MyString) String() string {
    // 错误，导致 无限的递归
    return fmt.Sprintf("MyString=%s", m) // Error: will recur forever.
}
```

It's also easy to fix: convert the argument to the basic string type, which does not have the method.
```go
type MyString string
func (m MyString) String() string {
    return fmt.Sprintf("MyString=%s", string(m)) // OK: note conversion.
}
```
In the initialization section we'll see another technique that avoids this recursion.


Another printing technique is to pass a print routine's arguments directly to another such routine. The signature of Printf uses the type ...interface{} for its final argument to specify that an arbitrary number of parameters (of arbitrary type) can appear after the format.

```go
func Printf(format string, v ...interface{}) (n int, err error) {
```

Within the function Printf, v acts like a variable of type []interface{} but if it is passed to another variadic function, it acts like a regular list of arguments. Here is the implementation of the function log.Println we used above. It passes its arguments directly to fmt.Sprintln for the actual formatting.

```go
// Println prints to the standard logger in the manner of fmt.Println.
func Println(v ...interface{}) {
    std.Output(2, fmt.Sprintln(v...))  // Output takes parameters (int, string)
}
```

We write ... after v in the nested call to Sprintln to tell the compiler to treat v as a list of arguments; otherwise it would just pass v as a single slice argument
> 写在 v 之后的 ... 用于告诉编译器将 v 视为 一列 arguments; 否则 其 将 v 作为 单个的 slice argument 传递。

There's even more to printing than we've covered here. See the godoc documentation for package fmt for the details.
```bash
$ go doc fmt
```

By the way, a ... parameter can be of a specific type, for instance ...int for a min function that chooses the least of a list of integers:
```go
func Min(a ...int) int {
    min := int(^uint(0) >> 1)  // largest int
    for _, i := range a {
        if i < min {
            min = i
        }
    }
    return min
}
```

#### Append

Now we have the missing piece we needed to explain the design of the append built-in function. The signature of append is different from our custom Append function above. Schematically, it's like this:

```go
func append(slice []T, elements ...T) []T
```

where T is a placeholder for any given type. You can't actually write a function in Go where the type T is determined by the caller. That's why append is built in: it needs support from the compiler.
> 此处 T 是任意给定 type 的 占位符。在 Go 中实际上你无法编写 有 其 类型 T 有 caller 确定的 a function. 这也是 为什么为 内置函数的原因：其需要 compiler 的支持。

What append does is append the elements to the end of the slice and return the result. The result needs to be returned because, as with our hand-written Append, the underlying array may change. This simple example

```go
x := []int{1,2,3}
x = append(x, 4, 5, 6)
fmt.Println(x)
```

prints [1 2 3 4 5 6]. So append works a little like Printf, collecting an arbitrary number of arguments.

But what if we wanted to do what our Append does and append a slice to a slice? Easy: use ... at the call site, just as we did in the call to Output above. This snippet produces identical output to the one above.

```go
x := []int{1,2,3}
y := []int{4,5,6}
x = append(x, y...)
fmt.Println(x)
```

Without that ..., it wouldn't compile because the types would be wrong; y is not of type int.


#### Initialization 

Although it doesn't look superficially very different from initialization in C or C++, initialization in Go is more powerful. Complex structures can be built during initialization and the ordering issues among initialized objects, even among different packages, are handled correctly.


#### Constants 

Constants in Go are just that—constant. They are created at compile time, even when defined as locals in functions, and can only be numbers, characters (runes), strings or booleans. Because of the compile-time restriction, the expressions that define them must be constant expressions, evaluatable by the compiler. For instance, 1<<3 is a constant expression, while math.Sin(math.Pi/4) is not because the function call to math.Sin needs to happen at run time.
> Constants（常量） 是在 编译时 被创建的，即使其是作为 locals 在 functions 中所定义的， 且 仅可以是 numbers, characters (runes), strings 和 booleans. 因为编译时的约束， 所以用于定义 Constants 的 表达式也必须是 常量表达式。


In Go, enumerated constants are created using the iota enumerator. Since iota can be part of an expression and expressions can be implicitly repeated, it is easy to build intricate sets of values.

```go
type ByteSize float64

const (
    _           = iota // ignore first value by assigning to blank identifier
    KB ByteSize = 1 << (10 * iota)
    MB
    GB
    TB
    PB
    EB
    ZB
    YB
)
```

The ability to attach a method such as String to any user-defined type makes it possible for arbitrary values to format themselves automatically for printing. Although you'll see it most often applied to structs, this technique is also useful for scalar types such as floating-point types like ByteSize.

```go
func (b ByteSize) String() string {
    switch {
    case b >= YB:
        return fmt.Sprintf("%.2fYB", b/YB)
    case b >= ZB:
        return fmt.Sprintf("%.2fZB", b/ZB)
    case b >= EB:
        return fmt.Sprintf("%.2fEB", b/EB)
    case b >= PB:
        return fmt.Sprintf("%.2fPB", b/PB)
    case b >= TB:
        return fmt.Sprintf("%.2fTB", b/TB)
    case b >= GB:
        return fmt.Sprintf("%.2fGB", b/GB)
    case b >= MB:
        return fmt.Sprintf("%.2fMB", b/MB)
    case b >= KB:
        return fmt.Sprintf("%.2fKB", b/KB)
    }
    return fmt.Sprintf("%.2fB", b)
}
```

The expression YB prints as 1.00YB, while ByteSize(1e13) prints as 9.09TB.

The use here of Sprintf to implement ByteSize's String method is safe (avoids recurring indefinitely) not because of a conversion but because it calls Sprintf with %f, which is not a string format: Sprintf will only call the String method when it wants a string, and %f wants a floating-point value.


#### Variables

Variables can be initialized just like constants but the initializer can be a general expression computed at run time.

> Variables 可以像 constants 那样被初始化 但是 其 初始化式 可以是 在 run time 时 计算的 通用 expression.

```go
var (
    home   = os.Getenv("HOME")
    user   = os.Getenv("USER")
    gopath = os.Getenv("GOPATH")
)
```

#### The init function

Finally, each source file can define its own niladic init function to set up whatever state is required. (Actually each file can have multiple init functions.) And finally means finally: init is called after all the variable declarations in the package have evaluated their initializers, and those are evaluated only after all the imported packages have been initialized.


Besides initializations that cannot be expressed as declarations, a common use of init functions is to verify or repair correctness of the program state before real execution begins.

```go
func init() {
    if user == "" {
        log.Fatal("$USER not set")
    }
    if home == "" {
        home = "/home/" + user
    }
    if gopath == "" {
        gopath = home + "/go"
    }
    // gopath may be overridden by --gopath flag on command line.
    flag.StringVar(&gopath, "gopath", gopath, "override default GOPATH")
}
```

### Methods

#### Pointers vs. Values

As we saw with ByteSize, methods can be defined for any named type (except a pointer or an interface); the receiver does not have to be a struct.


In the discussion of slices above, we wrote an Append function. We can define it as a method on slices instead. To do this, we first declare a named type to which we can bind the method, and then make the receiver for the method a value of that type.

```go
type ByteSlice []byte

func (slice ByteSlice) Append(data []byte) []byte {
    // Body exactly the same as the Append function defined above.
}
```

This still requires the method to return the updated slice. We can eliminate that clumsiness by redefining the method to take a pointer to a ByteSlice as its receiver, so the method can overwrite the caller's slice.

```go
func (p *ByteSlice) Append(data []byte) {
    slice := *p
    // Body as above, without the return.
    *p = slice
}
```

In fact, we can do even better. If we modify our function so it looks like a standard Write method, like this,

```go
func (p *ByteSlice) Write(data []byte) (n int, err error) {
    slice := *p
    // Again as above.
    *p = slice
    return len(data), nil
}
```

then the type *ByteSlice satisfies the standard interface io.Writer, which is handy. For instance, we can print into one.

```go
    var b ByteSlice
    fmt.Fprintf(&b, "This hour has %d days\n", 7)
```

We pass the address of a ByteSlice because only *ByteSlice satisfies io.Writer. The rule about pointers vs. values for receivers is that value methods can be invoked on pointers and values, but pointer methods can only be invoked on pointers.


This rule arises because pointer methods can modify the receiver; invoking them on a value would cause the method to receive a copy of the value, so any modifications would be discarded. The language therefore disallows this mistake. There is a handy exception, though. When the value is addressable, the language takes care of the common case of invoking a pointer method on a value by inserting the address operator automatically. In our example, the variable b is addressable, so we can call its Write method with just b.Write. The compiler will rewrite that to (&b).Write for us.


By the way, the idea of using Write on a slice of bytes is central to the implementation of bytes.Buffer.


### Interfaces and other types

#### Interfaces

Interfaces in Go provide a way to specify the behavior of an object: if something can do this, then it can be used here. We've seen a couple of simple examples already; custom printers can be implemented by a String method while Fprintf can generate output to anything with a Write method. Interfaces with only one or two methods are common in Go code, and are usually given a name derived from the method, such as io.Writer for something that implements Write.


A type can implement multiple interfaces. For instance, a collection can be sorted by the routines in package sort if it implements sort.Interface, which contains Len(), Less(i, j int) bool, and Swap(i, j int), and it could also have a custom formatter. In this contrived example Sequence satisfies both.


```go
type Sequence []int

// Methods required by sort.Interface.
func (s Sequence) Len() int {
    return len(s)
}
func (s Sequence) Less(i, j int) bool {
    return s[i] < s[j]
}
func (s Sequence) Swap(i, j int) {
    s[i], s[j] = s[j], s[i]
}

// Copy returns a copy of the Sequence.
func (s Sequence) Copy() Sequence {
    copy := make(Sequence, 0, len(s))
    return append(copy, s...)
}

// Method for printing - sorts the elements before printing.
func (s Sequence) String() string {
    s = s.Copy() // Make a copy; don't overwrite argument.
    sort.Sort(s)
    str := "["
    for i, elem := range s { // Loop is O(N²); will fix that in next example.
        if i > 0 {
            str += " "
        }
        str += fmt.Sprint(elem)
    }
    return str + "]"
}
```

#### Conversions

The String method of Sequence is recreating the work that Sprint already does for slices. (It also has complexity O(N²), which is poor.) We can share the effort (and also speed it up) if we convert the Sequence to a plain []int before calling Sprint.

```go
func (s Sequence) String() string {
    s = s.Copy()
    sort.Sort(s)
    return fmt.Sprint([]int(s))
}
```

This method is another example of the conversion technique for calling Sprintf safely from a String method. Because the two types (Sequence and []int) are the same if we ignore the type name, it's legal to convert between them. The conversion doesn't create a new value, it just temporarily acts as though the existing value has a new type. (There are other legal conversions, such as from integer to floating point, that do create a new value.)
> 因为如果忽略掉 type name 则这两个 types (Sequence and []int) 就是相同的，所以在它们之间进行类型转换时合法的。该 转换(conversion) 不会创建 a new value, 其仅是临时表现为就像 该 existing value 具有 a new type.(还存在其他的合法转换，例如从 integer 到 floating point 的转换，其会创建 a new value)


Now, instead of having Sequence implement multiple interfaces (sorting and printing), we're using the ability of a data item to be converted to multiple types (Sequence, sort.IntSlice and []int), each of which does some part of the job. That's more unusual in practice but can be effective.



#### Interface conversions and type assertions

Type switches are a form of conversion: they take an interface and, for each case in the switch, in a sense convert it to the type of that case. Here's a simplified version of how the code under fmt.Printf turns a value into a string using a type switch. If it's already a string, we want the actual string value held by the interface, while if it has a String method we want the result of calling the method.
> Type switches 是 conversion 的一种形式。

```go
type Stringer interface {
    String() string
}

var value interface{} // Value provided by caller.
switch str := value.(type) { //注: 此处使用了关键字 type
case string:
    return str
case Stringer:
    return str.String()
}
```

The first case finds a concrete value; the second converts the interface into another interface. It's perfectly fine to mix types this way.

What if there's only one type we care about? If we know the value holds a string and we just want to extract it? A one-case type switch would do, but so would a type assertion. A type assertion takes an interface value and extracts from it a value of the specified explicit type. The syntax borrows from the clause opening a type switch, but with an explicit type rather than the type keyword:


What if there's only one type we care about? If we know the value holds a string and we just want to extract it? A one-case type switch would do, but so would a type assertion. A type assertion takes an interface value and extracts from it a value of the specified explicit type. The syntax borrows from the clause opening a type switch, but with an explicit type rather than the type keyword:

```go
value.(typeName) //注: 类型断言 使用的是 typeName(即某个类型的名字), 而不是使用的关键字 type
```


and the result is a new value with the static type typeName. That type must either be the concrete type held by the interface, or a second interface type that the value can be converted to. To extract the string we know is in the value, we could write:
```go
str := value.(string)
```

But if it turns out that the value does not contain a string, the program will crash with a run-time error. To guard against that, use the "comma, ok" idiom to test, safely, whether the value is a string:
```go
str, ok := value.(string)  // "comma, ok" 惯用法 //如果转换失败，str 为 类型 string 的 zero value
if ok {
    fmt.Printf("string value is: %q\n", str)
} else {
    fmt.Printf("value is not a string\n")
}
```
If the type assertion fails, str will still exist and be of type string, but it will have the zero value, an empty string.

As an illustration of the capability, here's an if-else statement that's equivalent to the type switch that opened this section.
```go
if str, ok := value.(string); ok {
    return str
} else if str, ok := value.(Stringer); ok {
    return str.String()
}
```


#### Generality

If a type exists only to implement an interface and will never have exported methods beyond that interface, there is no need to export the type itself. Exporting just the interface makes it clear the value has no interesting behavior beyond what is described in the interface. It also avoids the need to repeat the documentation on every instance of a common method.


In such cases, the constructor should return an interface value rather than the implementing type. As an example, in the hash libraries both crc32.NewIEEE and adler32.New return the interface type hash.Hash32. Substituting the CRC-32 algorithm for Adler-32 in a Go program requires only changing the constructor call; the rest of the code is unaffected by the change of algorithm.


A similar approach allows the streaming cipher algorithms in the various crypto packages to be separated from the block ciphers they chain together. The Block interface in the crypto/cipher package specifies the behavior of a block cipher, which provides encryption of a single block of data. Then, by analogy with the bufio package, cipher packages that implement this interface can be used to construct streaming ciphers, represented by the Stream interface, without knowing the details of the block encryption.


The crypto/cipher interfaces look like this:

```go
type Block interface {
    BlockSize() int
    Encrypt(dst, src []byte)
    Decrypt(dst, src []byte)
}

type Stream interface {
    XORKeyStream(dst, src []byte)
}
```

Here's the definition of the counter mode (CTR) stream, which turns a block cipher into a streaming cipher; notice that the block cipher's details are abstracted away:

```go
// NewCTR returns a Stream that encrypts/decrypts using the given Block in
// counter mode. The length of iv must be the same as the Block's block size.
func NewCTR(block Block, iv []byte) Stream
```

NewCTR applies not just to one specific encryption algorithm and data source but to any implementation of the Block interface and any Stream. Because they return interface values, replacing CTR encryption with other encryption modes is a localized change. The constructor calls must be edited, but because the surrounding code must treat the result only as a Stream, it won't notice the difference.

#### Interfaces and methods

Since almost anything can have methods attached, almost anything can satisfy an interface. One illustrative example is in the http package, which defines the Handler interface. Any object that implements Handler can serve HTTP requests.

```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```

ResponseWriter is itself an interface that provides access to the methods needed to return the response to the client. Those methods include the standard Write method, so an http.ResponseWriter can be used wherever an io.Writer can be used. Request is a struct containing a parsed representation of the request from the client.


For brevity, let's ignore POSTs and assume HTTP requests are always GETs; that simplification does not affect the way the handlers are set up. Here's a trivial implementation of a handler to count the number of times the page is visited.

```go
// Simple counter server.
type Counter struct {
    n int
}

func (ctr *Counter) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    ctr.n++
    fmt.Fprintf(w, "counter = %d\n", ctr.n)
}
```


(Keeping with our theme, note how Fprintf can print to an http.ResponseWriter.) In a real server, access to ctr.n would need protection from concurrent access. See the sync and atomic packages for suggestions.


For reference, here's how to attach such a server to a node on the URL tree.

```go
import "net/http"
...
ctr := new(Counter)
http.Handle("/counter", ctr)
```


But why make Counter a struct? An integer is all that's needed. (The receiver needs to be a pointer so the increment is visible to the caller.)

```go
// Simpler counter server.
type Counter int

func (ctr *Counter) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    *ctr++
    fmt.Fprintf(w, "counter = %d\n", *ctr)
}
```

What if your program has some internal state that needs to be notified that a page has been visited? Tie a channel to the web page.

```go
// A channel that sends a notification on each visit.
// (Probably want the channel to be buffered.)
type Chan chan *http.Request

func (ch Chan) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    ch <- req
    fmt.Fprint(w, "notification sent")
}
```

Finally, let's say we wanted to present on /args the arguments used when invoking the server binary. It's easy to write a function to print the arguments.

```go
func ArgServer() {
    fmt.Println(os.Args)
}
```

How do we turn that into an HTTP server? We could make ArgServer a method of some type whose value we ignore, but there's a cleaner way. Since we can define a method for any type except pointers and interfaces, we can write a method for a function. The http package contains this code:

> 我们可以为 除 pointers 和 interfaces 的任意类型定义 a method

```go
// The HandlerFunc type is an adapter to allow the use of
// ordinary functions as HTTP handlers.  If f is a function
// with the appropriate signature, HandlerFunc(f) is a
// Handler object that calls f.
type HandlerFunc func(ResponseWriter, *Request)

// ServeHTTP calls f(w, req).
func (f HandlerFunc) ServeHTTP(w ResponseWriter, req *Request) {
    f(w, req)
}
```

HandlerFunc is a type with a method, ServeHTTP, so values of that type can serve HTTP requests. Look at the implementation of the method: the receiver is a function, f, and the method calls f. That may seem odd but it's not that different from, say, the receiver being a channel and the method sending on the channel.

To make ArgServer into an HTTP server, we first modify it to have the right signature.

```go
// Argument server.
func ArgServer(w http.ResponseWriter, req *http.Request) {
    fmt.Fprintln(w, os.Args)
}
```

```go
http.Handle("/args", http.HandlerFunc(ArgServer))
```

When someone visits the page /args, the handler installed at that page has value ArgServer and type HandlerFunc. The HTTP server will invoke the method ServeHTTP of that type, with ArgServer as the receiver, which will in turn call ArgServer (via the invocation f(w, req) inside HandlerFunc.ServeHTTP). The arguments will then be displayed.


In this section we have made an HTTP server from a struct, an integer, a channel, and a function, all because interfaces are just sets of methods, which can be defined for (almost) any type.



### The blank identifier: 空白标识符

We've mentioned the blank identifier a couple of times now, in the context of for range loops and maps. The blank identifier can be assigned or declared with any value of any type, with the value discarded harmlessly. It's a bit like writing to the Unix /dev/null file: it represents a write-only value to be used as a place-holder where a variable is needed but the actual value is irrelevant. It has uses beyond those we've seen already.

> 空白标识符 _ 有点类似于 unix 中的 /dev/null 文件，它代表 a write-only value.

#### The blank identifier in multiple assignment

The use of a blank identifier in a for range loop is a special case of a general situation: multiple assignment.


If an assignment requires multiple values on the left side, but one of the values will not be used by the program, a blank identifier on the left-hand-side of the assignment avoids the need to create a dummy variable and makes it clear that the value is to be discarded. For instance, when calling a function that returns a value and an error, but only the error is important, use the blank identifier to discard the irrelevant value.

```go

// 使用空白标识符 _ 丢弃 不想要的 value
if _, err := os.Stat(path); os.IsNotExist(err) {
	fmt.Printf("%s does not exist\n", path)
}
```

Occasionally you'll see code that discards the error value in order to ignore the error; this is terrible practice. Always check error returns; they're provided for a reason.

```go
// Bad! This code will crash if path does not exist.
fi, _ := os.Stat(path) //错误，该  code 在 path 不存在时对 崩溃
if fi.IsDir() {
    fmt.Printf("%s is a directory\n", path)
}
```


#### Unused imports and variables

It is an error to import a package or to declare a variable without using it. Unused imports bloat the program and slow compilation, while a variable that is initialized but not used is at least a wasted computation and perhaps indicative of a larger bug. When a program is under active development, however, unused imports and variables often arise and it can be annoying to delete them just to have the compilation proceed, only to have them be needed again later. The blank identifier provides a workaround.


This half-written program has two unused imports (fmt and io) and an unused variable (fd), so it will not compile, but it would be nice to see if the code so far is correct.


```go
package main

import (
    "fmt"
    "io"
    "log"
    "os"
)

func main() {
    fd, err := os.Open("test.go")
    if err != nil {
        log.Fatal(err)
    }
    // TODO: use fd.
}

```

To silence complaints about the unused imports, use a blank identifier to refer to a symbol from the imported package. Similarly, assigning the unused variable fd to the blank identifier will silence the unused variable error. This version of the program does compile.

```go
package main

import (
    "fmt"
    "io"
    "log"
    "os"
)

var _ = fmt.Printf // For debugging; delete when done.
var _ io.Reader    // For debugging; delete when done.

func main() {
    fd, err := os.Open("test.go")
    if err != nil {
        log.Fatal(err)
    }
    // TODO: use fd.
    _ = fd
}
```

By convention, the global declarations to silence import errors should come right after the imports and be commented, both to make them easy to find and as a reminder to clean things up later.



#### Import for side effect

An unused import like fmt or io in the previous example should eventually be used or removed: blank assignments identify code as a work in progress. But sometimes it is useful to import a package only for its side effects, without any explicit use. For example, during its init function, the net/http/pprof package registers HTTP handlers that provide debugging information. It has an exported API, but most clients need only the handler registration and access the data through a web page. To import the package only for its side effects, rename the package to the blank identifier:


```go
import _ "net/http/pprof"
```

This form of import makes clear that the package is being imported for its side effects, because there is no other possible use of the package: in this file, it doesn't have a name. (If it did, and we didn't use that name, the compiler would reject the program.)


#### Interface checks

As we saw in the discussion of interfaces above, a type need not declare explicitly that it implements an interface. Instead, a type implements the interface just by implementing the interface's methods. In practice, most interface conversions are static and therefore checked at compile time. For example, passing an *os.File to a function expecting an io.Reader will not compile unless *os.File implements the io.Reader interface.


Some interface checks do happen at run-time, though. One instance is in the encoding/json package, which defines a Marshaler interface. When the JSON encoder receives a value that implements that interface, the encoder invokes the value's marshaling method to convert it to JSON instead of doing the standard conversion. The encoder checks this property at run time with a type assertion like:

```go
m, ok := val.(json.Marshaler)
```

If it's necessary only to ask whether a type implements an interface, without actually using the interface itself, perhaps as part of an error check, use the blank identifier to ignore the type-asserted value:

```go
if _, ok := val.(json.Marshaler); ok {
    fmt.Printf("value %v of type %T implements json.Marshaler\n", val, val)
}
```

One place this situation arises is when it is necessary to guarantee within the package implementing the type that it actually satisfies the interface. If a type—for example, json.RawMessage—needs a custom JSON representation, it should implement json.Marshaler, but there are no static conversions that would cause the compiler to verify this automatically. If the type inadvertently fails to satisfy the interface, the JSON encoder will still work, but will not use the custom implementation. To guarantee that the implementation is correct, a global declaration using the blank identifier can be used in the package:

```go
var _ json.Marshaler = (*RawMessage)(nil)
```

In this declaration, the assignment involving a conversion of a *RawMessage to a Marshaler requires that *RawMessage implements Marshaler, and that property will be checked at compile time. Should the json.Marshaler interface change, this package will no longer compile and we will be on notice that it needs to be updated.

The appearance of the blank identifier in this construct indicates that the declaration exists only for the type checking, not to create a variable. Don't do this for every type that satisfies an interface, though. By convention, such declarations are only used when there are no static conversions already present in the code, which is a rare event.

### Embedding

Go does not provide the typical, type-driven notion of subclassing, but it does have the ability to “borrow” pieces of an implementation by embedding types within a struct or interface.

Interface embedding is very simple. We've mentioned the io.Reader and io.Writer interfaces before; here are their definitions.


```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}
```

The io package also exports several other interfaces that specify objects that can implement several such methods. For instance, there is io.ReadWriter, an interface containing both Read and Write. We could specify io.ReadWriter by listing the two methods explicitly, but it's easier and more evocative to embed the two interfaces to form the new one, like this:

```go
// ReadWriter is the interface that combines the Reader and Writer interfaces.
type ReadWriter interface {
    Reader
    Writer
}
```

This says just what it looks like: A ReadWriter can do what a Reader does and what a Writer does; it is a union of the embedded interfaces. Only interfaces can be embedded within interfaces.
> 仅 interfaces 可以被嵌入到 interfaces 中

The same basic idea applies to structs, but with more far-reaching implications. The bufio package has two struct types, bufio.Reader and bufio.Writer, each of which of course implements the analogous interfaces from package io. And bufio also implements a buffered reader/writer, which it does by combining a reader and a writer into one struct using embedding: it lists the types within the struct but does not give them field names.

```go
// ReadWriter stores pointers to a Reader and a Writer.
// It implements io.ReadWriter.
type ReadWriter struct {
    *Reader  // *bufio.Reader
    *Writer  // *bufio.Writer
}
```

The embedded elements are pointers to structs and of course must be initialized to point to valid structs before they can be used. The ReadWriter struct could be written as


```go
type ReadWriter struct {
    reader *Reader
    writer *Writer
}
```

but then to promote the methods of the fields and to satisfy the io interfaces, we would also need to provide forwarding methods, like this:

```go
func (rw *ReadWriter) Read(p []byte) (n int, err error) {
    return rw.reader.Read(p)
}
```

By embedding the structs directly, we avoid this bookkeeping. The methods of embedded types come along for free, which means that bufio.ReadWriter not only has the methods of bufio.Reader and bufio.Writer, it also satisfies all three interfaces: io.Reader, io.Writer, and io.ReadWriter.

> 注意 embedding 与 subclassing 的区别
There's an important way in which embedding differs from subclassing. When we embed a type, the methods of that type become methods of the outer type, but when they are invoked the receiver of the method is the inner type, not the outer one. In our example, when the Read method of a bufio.ReadWriter is invoked, it has exactly the same effect as the forwarding method written out above; the receiver is the reader field of the ReadWriter, not the ReadWriter itself.

Embedding can also be a simple convenience. This example shows an embedded field alongside a regular, named field.

```go
type Job struct {
    Command string
    *log.Logger
}
```

The Job type now has the Print, Printf, Println and other methods of *log.Logger. We could have given the Logger a field name, of course, but it's not necessary to do so. And now, once initialized, we can log to the Job:

```go
job.Println("starting now...")
```

The Logger is a regular field of the Job struct, so we can initialize it in the usual way inside the constructor for Job, like this,


```go
func NewJob(command string, logger *log.Logger) *Job {
    return &Job{command, logger}
}
```

or with a composite literal,

```go
job := &Job{command, log.New(os.Stderr, "Job: ", log.Ldate)}
```

If we need to refer to an embedded field directly, the type name of the field, ignoring the package qualifier, serves as a field name, as it did in the Read method of our ReadWriter struct. Here, if we needed to access the *log.Logger of a Job variable job, we would write job.Logger, which would be useful if we wanted to refine the methods of Logger.

```go
func (job *Job) Printf(format string, args ...interface{}) {
    job.Logger.Printf("%q: %s", job.Command, fmt.Sprintf(format, args...))
}
```

Embedding types introduces the problem of name conflicts but the rules to resolve them are simple. First, a field or method X hides any other item X in a more deeply nested part of the type. If log.Logger contained a field or method called Command, the Command field of Job would dominate it.


Second, if the same name appears at the same nesting level, it is usually an error; it would be erroneous to embed log.Logger if the Job struct contained another field or method called Logger. However, if the duplicate name is never mentioned in the program outside the type definition, it is OK. This qualification provides some protection against changes made to types embedded from outside; there is no problem if a field is added that conflicts with another field in another subtype if neither field is ever used.




















一些网上资料:

- Go by Example
	https://gobyexample.com/

- go语言开发规范建议以及开发过程中各种各样的坑
	https://www.toutiao.com/a6921504074407985671/

- 20 Best Golang Books You Should Read
	https://golangexample.com/20-golang-books/

- 李文周的博客
	https://www.liwenzhou.com/
	https://www.liwenzhou.com/posts/Go/go_menu/


- Golang：数据库ORM框架GoMybatis详解 (废弃, 因为 GoMyBatis 好像不能像 java
		的 mybatis 那样支持 多表查询, 所以可能还是选择其他 框架好一些)
  https://studygolang.com/articles/22386?utm_source=tuicool&utm_medium=referral
	https://pkg.go.dev/github.com/zhuxiujia/GoMybatis

-	学些 GoMybatis 之前还是应该先学习 java 的 mybatis
	https://mybatis.org/mybatis-3/







```go
/*
https://www.liwenzhou.com/

Go 语言中函数的 return 不是原子操作，在底层是分为两步来执行
第一步: 返回值赋值
第二步: 真正的 RET 返回
// 注: 函数中如果存在 defer, 那么 defer 所计划的 函数调用是在 第一步和第二步之间执行
*/

```


```go
// 参考book: <The Go Programming Language>
func f1() {
	x := 100

	if x := 1; true {
		fmt.Println(x) //output: 1
		x := 4
		fmt.Println(x) //output: 4
	}

	fmt.Println(x) //output: 100
}
```


```go
// 参考book: <The Go Programming Language>
func main() {
	f1()
}

func f1() {
	for i := 0; i < 3; i++ {
		defer func() {
			fmt.Println("first defer: ", i)
		}()
	}

	for i := 0; i < 3; i++ {
		defer func(i int) {
			fmt.Println("second defer: ", i)
		}(i)
	}

	/*output:
	second defer:  2
	second defer:  1
	second defer:  0
	first defer:  3
	first defer:  3
	first defer:  3
```


```go
// 类型别名
// https://yourbasic.org/golang/type-alias/
// https://golang.google.cn/ref/spec#Type_declarations



// /app/go/src/builtin/builtin.go
type byte = uint8
type rune = int32


```


[Anonymous Structure and Field in Golang](https://www.geeksforgeeks.org/anonymous-structure-and-field-in-golang/#:~:text=In%20Go%20language%2C%20you%20are%20allowed%20to%20create,%3A%3D%20struct%20%7B%20%2F%2F%20fields%20%7D%20%7B%2F%2F%20Field_values%7D)
```go
// 匿名结构体
var person struct {
	name string
	age  int8
}
```


























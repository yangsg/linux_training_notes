

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


- 一些 java 中 的数据库使用方式:
	https://zhuanlan.zhihu.com/p/263043522

	MyBatis FreeMarker: http://mybatis.org/freemarker-scripting/#
	sagacity-sqltoy: https://github.com/sagframe/sagacity-sqltoy
                   https://github.com/sagframe
                   https://gitee.com/sagacity/sagacity-sqltoy





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


- 关于 time 的 Format 和 Parse 方法/函数 的一个小 demo
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()
	fmt.Printf("fmt.Printf now: %s\n", now)
	//output: fmt.Printf now: 2021-02-18 14:35:29.09133989 +0800 CST m=+0.000043098

	var nowStr string
	nowStr = now.Format("2006-01-02 15:04:05.999999999 -0700 MST")
	fmt.Printf("format nowStr01：%s\n", nowStr)
	//output: format nowStr01：2021-02-18 14:35:29.09133989 +0800 CST

	nowStr = now.Format("2006-01-02 15:04:05.999999999 -0700")
	fmt.Printf("format nowStr02：%s\n", nowStr)
	//output: format nowStr02：2021-02-18 14:35:29.09133989 +0800

	time01, _ := time.Parse("2006-01-02 15:04:05.999999999 -0700", "2021-02-18 14:26:43.944726887 +0800")
	fmt.Printf("parsed time01 is %v\n", time01)
	//output: parsed time01 is 2021-02-18 14:26:43.944726887 +0800 CST
}

```

- 关于 mysql 的 INSERT ... ON DUPLICATE KEY UPDATE 语句介绍(注: 类似 gorm 这种 orm 框架会利用到)
		> - [来自mysql8官方文档](https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html)
    > - [来自javatpoint](https://www.javatpoint.com/mysql-insert-on-duplicate-key-update#:~:text=The%20Insert%20on%20Duplicate%20Key%20Update%20statement%20is,column%2C%20then%20updation%20of%20the%20existing%20row%20occurs.)



###### 注: 关于实际中对 Restful Api 的处理：
现实中完全遵守 Restful Api 规范可能有点困难, 因为偶尔会引起某些问题(如某些浏览器 bug, 防火墙设置等)
或 使某些处理复杂化, 所以作为妥协，可能还是最好仅使用 GET 和  POST 两种方法, 不过也许
可以借用 Restful Api 的一些想法，将某些 Api 定义成类似如下这种方式:
```text
功能              HTTP方法            路径
-------------------------------------------------------
新增用户           POST               /post/users
删除指定用户       POST               /delete/users/:id
更新指定用户       POST               /put/users/:id
更新指定用户某部分 POST               /patch/users/:id/state
获取用户列表       GET                /get/users
获取指定用户       GET                /get/users/:id
```



##### MySQL Workbench 中对 database 的 逆向工程(Reverse Engineering)
	- https://dataedo.com/kb/tools/mysql-workbench/create-database-diagram
	- https://dataedo.com/kb/tools/mysql-workbench/how-to-reverse-engineer-database






















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




























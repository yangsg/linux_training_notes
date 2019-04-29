#!/bin/bash


# keyword function


# man bash  #/   Shell Function Definitions


#// 函数定义
#// 语法: name () compound-command [redirection]
#// 语法: function name [()] compound-command [redirection]      #<<< 推荐这种，可读性更好一些

#// 注：bash 中 function 编码时只能先定义 后 使用

function fn_say_hello()
{
  echo 'hello world'
}

fn_say_hello


function fn_write_file()   # 一个定义时带有重定向的函数
{

  echo 'fn_write_file'
  date '+%F_%T'
} >> /tmp/fn_write_file.log

fn_write_file

function fn_do_nothing()
{
  :     # 命令 : 是 Null command
}

fn_do_nothing

function fn_sum()  # 调用方式: fn_sum 1 2
{
  echo $(($1 + $2))
}

fn_sum 1 2

message=Hello
Hello=Goodbye
function fn_echo_var()
{
  echo "$1"
}

fn_echo_var "$message"
fn_echo_var "${!message}"   # 间接引用

function fn_return_exit_status()
{
  return 1   # 如果function没有return 语句, 则function 默认的exit status 为其最后执行的命令的 exit status
}

fn_return_exit_status

if [ $? -eq 0 ]; then
  echo 'success'
else
  echo 'fail'
fi

function fn_echo_local_var()
{
   local name
   name='Bob'

   local age=25

   echo "$name $age"
}

fn_echo_local_var


function fn_echo_positional_parameters()
{
  for var in "$@"; do
    echo -n "$var "
  done

  echo
  echo "number of positional parameters is: ${#@}"
  echo "number of positional parameters is: ${#*}"
  echo "number of positional parameters is: $#"
}

fn_echo_positional_parameters  a b
fn_echo_positional_parameters  a b e f g
fn_echo_positional_parameters  a b e f g 'h i j k l m n'

# function 的更多用法见 《Advanced Bash-Scripting Guide》


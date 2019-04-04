```
mysql> help set
Name: 'SET'
Description:
Syntax:
SET variable = expr [, variable = expr] ...

variable: {
    user_var_name
  | param_name
  | local_var_name
  | {GLOBAL | @@GLOBAL.} system_var_name
  | [SESSION | @@SESSION. | @@] system_var_name
}

SET syntax for variable assignment enables you to assign values to
different types of variables that affect the operation of the server or
clients:

o User-defined variables. See
  http://dev.mysql.com/doc/refman/5.7/en/user-variables.html.

o Stored procedure and function parameters, and stored program local
  variables. See
  http://dev.mysql.com/doc/refman/5.7/en/stored-program-variables.html.

o System variables. See
  http://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html.
  System variables also can be set at server startup, as described in
  http://dev.mysql.com/doc/refman/5.7/en/using-system-variables.html.

URL: http://dev.mysql.com/doc/refman/5.7/en/set-variable.html

```

```
mysql> select @@global.sql_log_bin, @@session.sql_log_bin;
+----------------------+-----------------------+
| @@global.sql_log_bin | @@session.sql_log_bin |
+----------------------+-----------------------+
|                    1 |                     1 |
+----------------------+-----------------------+

mysql> set @@session.sql_log_bin = OFF;

mysql> select @@global.sql_log_bin, @@session.sql_log_bin;
+----------------------+-----------------------+
| @@global.sql_log_bin | @@session.sql_log_bin |
+----------------------+-----------------------+
|                    1 |                     0 |
+----------------------+-----------------------+

mysql> set session sql_log_bin = ON;

mysql> select @@global.sql_log_bin, @@session.sql_log_bin;
+----------------------+-----------------------+
| @@global.sql_log_bin | @@session.sql_log_bin |
+----------------------+-----------------------+
|                    1 |                     1 |
+----------------------+-----------------------+


mysql> set sql_log_bin = OFF;

mysql> select @@global.sql_log_bin, @@session.sql_log_bin;
+----------------------+-----------------------+
| @@global.sql_log_bin | @@session.sql_log_bin |
+----------------------+-----------------------+
|                    1 |                     0 |
+----------------------+-----------------------+




```




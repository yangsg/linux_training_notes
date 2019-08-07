


- [Spanning multi-valued relationships](https://docs.djangoproject.com/en/2.2/topics/db/queries/#spanning-multi-valued-relationships)

```python3
Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
```
对应的 mysql 的 sql 语句:
```mysql
SELECT `myapp_blog`.`id` ,
       `myapp_blog`.`name`,
       `myapp_blog`.`tagline`
FROM `myapp_blog`
INNER JOIN `myapp_entry` ON (`myapp_blog`.`id` = `myapp_entry`.`blog_id`)
WHERE (`myapp_entry`.`headline` LIKE BINARY %Lennon%
       AND `myapp_entry`.`pub_date` BETWEEN 2008-01-01 AND 2008-12-31)
```

```python3
Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)
```
对应的 mysql 的 sql 语句:
```mysql
SELECT `myapp_blog`.`id`,
       `myapp_blog`.`name`,
       `myapp_blog`.`tagline`
FROM `myapp_blog`
INNER JOIN `myapp_entry` ON (`myapp_blog`.`id` = `myapp_entry`.`blog_id`)
INNER JOIN `myapp_entry` T3 ON (`myapp_blog`.`id` = T3.`blog_id`)
WHERE (`myapp_entry`.`headline` LIKE BINARY %Lennon%
       AND T3.`pub_date` BETWEEN 2008-01-01 AND 2008-12-31)
```



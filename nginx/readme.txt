
nginx 为什么比apache 性能更快，占用内存更少，见
   https://github.com/yangsg/linux_training_notes/tree/master/httpd/httpd01_server_basic


----------------------------------------------------------------------------------------
!!!!!!!!
nginx中关于location的一个很奇怪的特性，该特性如不注意在某些时刻很容易造成部署bug,所以在此记录下来：

官网地址  http://nginx.org/en/docs/http/ngx_http_core_module.html#location
有如下一段话：
  If a location is defined by a prefix string that ends with the slash character,
  and requests are processed by one of proxy_pass, fastcgi_pass, uwsgi_pass,
  scgi_pass, memcached_pass, or grpc_pass, then the special processing is performed.
  In response to a request with URI equal to this string, but without the trailing slash,
  a permanent redirect with the code 301 will be returned to the requested URI with the slash appended.
  If this is not desired, an exact match of the URI and location could be defined like this:

      location /user/ {
          proxy_pass http://user.example.com;
      }

      location = /user {
          proxy_pass http://login.example.com;
      }

即对于proxy_pass, fastcgi_pass, uwsgi_pass, scgi_pass, memcached_pass, or grpc_pass 处理的请求，
如果prefix string末尾以斜线‘/’结尾(如上面location /user/ 中的'/user/')，则这些各种的xxx_pass的
特殊处理可以得到执行。该请求的响应的URI等于该prefix string(如'/user/')。
但是如果prefix string没有以斜线符号'/'结尾(如上面location = /user 中的'/user')，则浏览器端会被
永久重定向(状态码为301)一个新的地址，即prefix string 末尾追加了斜线符号'/'得到的地址
(如上面中'/user' + '/' = '/user/')

注：上面官方的解决方案在某些情况下也有可能并不完美，
    因为重定向是无法浏览器两次请求之间自动保留请求信息的。

如上示例更多信息见
https://github.com/yangsg/linux_training_notes/blob/master/nginx/nginx02_server_basic/nginx7server/app/nginx/sites-available/location.match.demo.com.conf
----------------------------------------------------------------------------------------







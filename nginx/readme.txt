
nginx 为什么比apache 性能更快，占用内存更少，见
   https://github.com/yangsg/linux_training_notes/tree/master/httpd/httpd01_server_basic


介绍nginx中location配置规则非常好的一些文章，见
  https://artfulrobot.uk/blog/untangling-nginx-location-block-matching-algorithm
  https://www.digitalocean.com/community/tutorials/understanding-nginx-server-and-location-block-selection-algorithms




----------------------------------------------------------------------------------------
!!!!!!!!
nginx中关于location的一个特性，该特性如不注意在某些时刻很容易造成部署bug,所以在此记录下来：

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

----------------------------------------------------------------------------------------







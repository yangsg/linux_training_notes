


---------------------------------------------------------------------------------------------------
https://en.wikipedia.org/wiki/Common_Gateway_Interface

Common Gateway Interface (来自 wiki, 唉, 这么好的简单直白的解释, 却只能通过翻墙才能学习看到)

  In computing, Common Gateway Interface (CGI) offers a standard protocol for web servers to execute programs
  that execute like console applications (also called command-line interface programs) running on a server
  that generates web pages dynamically. Such programs are known as CGI scripts or simply as CGIs.
  The specifics of how the script is executed by the server are determined by the server.
  In the common case, a CGI script executes at the time a request is made and generates HTML.[1]

  In brief, an HTTP POST request from the client will send the HTML form data to the CGI program via standard input.
  Other data, such as URL paths, and HTTP header data, are presented as process environment variables.

  简而言之, 来自 client 的 an HTTP POST request 通过 standard input 将 the HTML form data 发送(send)给 the CGI program.
  其他 data, 如 URL paths, and HTTP header data, 被 表示为 进程 的 环境变量(environment variables).


The name CGI comes from the early days of the web, where users wanted to connect databases to their web servers.
The CGI was a program executed by the server that provided a common "gateway" between the web server and the database.


Using CGI scripts --------

A web server allows its owner to configure which URLs shall be handled by which CGI scripts.

    This is usually done by marking a new directory within the document collection
    as containing CGI scripts — its name is often cgi-bin.
    For example, /usr/local/apache/htdocs/cgi-bin could be designated as a CGI directory
    on the web server. When a Web browser requests a URL that points to a file
    within the CGI directory (e.g., http://example.com/cgi-bin/printenv.pl/with/additional/path?and=a&query=string),
    then, instead of simply sending that file (/usr/local/apache/htdocs/cgi-bin/printenv.pl) to the Web browser,
    the HTTP server runs the specified script and passes the output of the script to the Web browser.
    That is, anything that the script sends to standard output is passed to the Web client
    instead of being shown on-screen in a terminal window.


如下一些示例变量, 某些 (如 PATH_INFO, QUERY_STRING 等) 来自  CGI standard 定义, 某些(如以 HTTP_ 开头的变量)来自 HTTP request 传递的信息

   COMSPEC="C:\Windows\system32\cmd.exe"
   DOCUMENT_ROOT="C:/Program Files (x86)/Apache Software Foundation/Apache2.4/htdocs"
   GATEWAY_INTERFACE="CGI/1.1"
   HOME="/home/SYSTEM"
   HTTP_ACCEPT="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
   HTTP_ACCEPT_CHARSET="ISO-8859-1,utf-8;q=0.7,*;q=0.7"
   HTTP_ACCEPT_ENCODING="gzip, deflate, br"
   HTTP_ACCEPT_LANGUAGE="en-us,en;q=0.5"
   HTTP_CONNECTION="keep-alive"
   HTTP_HOST="example.com"
   HTTP_USER_AGENT="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0"
   PATH="/home/SYSTEM/bin:/bin:/cygdrive/c/progra~2/php:/cygdrive/c/windows/system32:..."
   PATHEXT=".COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC"
   PATH_INFO="/foo/bar"
   PATH_TRANSLATED="C:\Program Files (x86)\Apache Software Foundation\Apache2.4\htdocs\foo\bar"
   QUERY_STRING="var1=value1&var2=with%20percent%20encoding"
   REMOTE_ADDR="127.0.0.1"
   REMOTE_PORT="63555"
   REQUEST_METHOD="GET"
   REQUEST_URI="/cgi-bin/printenv.pl/foo/bar?var1=value1&var2=with%20percent%20encoding"
   SCRIPT_FILENAME="C:/Program Files (x86)/Apache Software Foundation/Apache2.4/cgi-bin/printenv.pl"
   SCRIPT_NAME="/cgi-bin/printenv.pl"
   SERVER_ADDR="127.0.0.1"
   SERVER_ADMIN="(server admin's email address)"
   SERVER_NAME="127.0.0.1"
   SERVER_PORT="80"
   SERVER_PROTOCOL="HTTP/1.1"
   SERVER_SIGNATURE=""
   SERVER_SOFTWARE="Apache/2.4.39 (Win32) PHP/7.3.7"
   SYSTEMROOT="C:\Windows"
   TERM="cygwin"
   WINDIR="C:\Windows"

-  Server specific variables:----------
-  SERVER_SOFTWARE:   name/version of HTTP server.
-  SERVER_NAME:       host name of the server, may be dot-decimal IP address.
-  GATEWAY_INTERFACE: CGI/version.
-  Request specific variables:---------
-  SERVER_PROTOCOL:   HTTP/version.
-  SERVER_PORT:       TCP port (decimal).
-  REQUEST_METHOD:    name of HTTP method (see above).
-  PATH_INFO:         path suffix, if appended to URL after program name and a slash.
-  PATH_TRANSLATED:   corresponding full path as supposed by server, if PATH_INFO is present.
-  SCRIPT_NAME:       relative path to the program, like /cgi-bin/script.cgi.
-  QUERY_STRING:      the part of URL after ? character. The query string may be composed of *name=value pairs separated
                   with ampersands (such as var1=val1&var2=val2...) when used to submit form data transferred
                   via GET method as defined by HTML application/x-www-form-urlencoded.
-  REMOTE_HOST:       host name of the client, unset if server did not perform such lookup.
-  REMOTE_ADDR:       IP address of the client (dot-decimal).
-  AUTH_TYPE:         identification type, if applicable.
-  REMOTE_USER used for certain AUTH_TYPEs.
-  REMOTE_IDENT:     see ident, only if server performed such lookup.
-  CONTENT_TYPE:     Internet media type of input data if PUT or POST method are used, as provided via HTTP header.
-  CONTENT_LENGTH:   similarly, size of input data (decimal, in octets) if provided via HTTP header.

Variables passed by user agent (HTTP_ACCEPT, HTTP_ACCEPT_LANGUAGE, HTTP_USER_AGENT, HTTP_COOKIE and possibly others) contain
values of corresponding HTTP headers and therefore have the same sense.


Deployment (部署, 以及一些通用的约定,习惯)
    A Web server that supports CGI can be configured to interpret a URL that it serves as a reference to a CGI script.
    A common convention is to have a cgi-bin/ directory at the base of the directory tree and
    treat all executable files within this directory (and no other, for security) as CGI scripts.
    Another popular convention is to use filename extensions; for instance,
    if CGI scripts are consistently given the extension .cgi, the web server can be configured
    to interpret all such files as CGI scripts. While convenient, and required by many prepackaged scripts,
    it opens the server to attack if a remote user can upload executable code with the proper extension.

    In the case of HTTP PUT or POSTs, the user-submitted data are provided to the program via the standard input.
    The Web server creates a subset of the environment variables passed to it and adds details pertinent to the HTTP environment.


Alternatives

    Calling a command generally means the invocation of a newly created process on the server.
    Starting the process can consume much more time and memory than the actual work of generating the output,
    especially when the program still needs to be interpreted or compiled.
    If the command is called often, the resulting workload can quickly overwhelm the server.

    The overhead involved in process creation can be reduced by techniques
    such as FastCGI that "prefork" interpreter processes, or
    by running the application code entirely within the web server,
    using extension modules such as mod_perl or mod_php.
    Another way to reduce the overhead is to use precompiled CGI programs,
    e.g. by writing them in languages such as C or C++, rather than interpreted or
    compiled-on-the-fly languages such as Perl or PHP, or
    by implementing the page generating software as a custom webserver module.

Alternative approaches include:

- Extensions:  such as Apache modules, NSAPI plugins, and ISAPI plugins allow third-party software to run on the web server.
               Web 2.0 allows to transfer data from the client to the server without using HTML forms and without the user noticing.[10]
-  FastCGI:    reduces overhead by allowing a single, long-running process to handle more than one user request.
               Unlike converting an application to a web server plug-in, FastCGI applications remain independent of the web server.

              FastCGI 通过 运行 单个(single)的, 长期运行的 进程(process) 处理 不只一个(即多个)的 user request.
              与 将 an application 转换为 a web server 的 插件(plug-in) 不同, FastCGI applications 存在 独立于 the web server.


-  Simple Common Gateway Interface or SCGI:  is designed to be easier to implement, yet it reduces latency in some operations compared to CGI.

-  Replacement of the architecture for dynamic websites can also be used (如 java servlet 容器).
              This is the approach taken by Java EE, which runs Java code in a Java servlet container
              in order to serve dynamic content and optionally static content.
              This approach replaces the overhead of generating and destroying processes
              with the much lower overhead of generating and destroying threads,
              and also exposes the programmer to the library that comes with Java Platform,
              Standard Edition on which the version of Java EE in use is based.

              Java servlet container 采用 threads(也被称为轻量级进程) 而非 笨重的 进程(processes) 提供 动态内容.

更多详细内容见 wiki
      https://en.wikipedia.org/wiki/Common_Gateway_Interface
---------------------------------------------------------------------------------------------------

https://en.wikipedia.org/wiki/FastCGI

FastCGI

    FastCGI is a binary protocol for interfacing interactive programs with a web server.
    It is a variation on the earlier Common Gateway Interface (CGI).
    FastCGI's main aim is to reduce the overhead related to interfacing between web server and CGI programs,
    allowing a server to handle more web page requests per unit of time.


    History-----------------------
      Common Gateway Interface (CGI) is a protocol for interfacing external applications to web servers.
      CGI applications run in separate processes, which are created at the start of
      each request and torn down at the end. This "one new process per request" model
      makes CGI programs very simple to implement, but limits efficiency and scalability.
      At high loads, the operating system overhead for process creation and destruction becomes significant.
      Also, the CGI process model limits resource reuse methods, such as reusing database connections, in-memory caching, etc.

    Implementation details-----------------------
        Instead of creating a new process for each request, FastCGI uses persistent processes to handle a series of requests.
        These processes are owned by the FastCGI server, not the web server.
        (这些 processes 属于 the FastCGI server, 而非 the web server)

        To service an incoming request, the web server sends environment variable information and
        the page request to a FastCGI process over either a Unix domain socket, a named pipe,
        or a Transmission Control Protocol (TCP) connection. Responses are returned from the process
        to the web server over the same connection, and the web server then delivers that response to the end user.
        The connection may be closed at the end of a response, but both web server and FastCGI service processes persist.[2]

        Each individual FastCGI process can handle many requests over its lifetime, thereby avoiding
        the overhead of per-request process creation and termination.
        Processing multiple requests concurrently can be done in several ways:
        by using one connection with internal multiplexing(多路复用) (i.e., multiple requests over one connection);多个请求通过通过一个 connection
        by using multiple connections(多个 connections); or by a mix of these methods(混合方式,即两种方式结合).
        Multiple FastCGI servers can be configured, increasing stability and scalability.

        多路复用( Multiplexing ):
            https://en.wikipedia.org/wiki/Multiplexing

        独立 部署 FastCGI 的优点:
        Web site administrators and programmers can find that separating web applications
        from the web server in FastCGI has many advantages over embedded interpreters (mod_perl, mod_php, etc.).
        This separation allows server and application processes to
        be restarted independently – an important consideration for busy web sites.
        It also enables the implementation of per-application, hosting service security policies,
        which is an important requirement for ISPs and web hosting companies.[3]
        Different types of incoming requests can be distributed to
        specific FastCGI servers which have been equipped to handle those types of requests efficiently.


---------------------------------------------------------------------------------------------------










https://djangodeployment.com/2016/11/15/why-nginx-is-faster-than-apache-and-why-you-neednt-necessarily-care/
Why nginx is faster than Apache, and why you needn’t necessarily care

    The big difference between the two servers is that Apache uses one thread per request, whereas nginx is event-driven.
    Apache(即httpd):采用"synchronous blocking I/O",多线程工作模式
    Nginx: 采用基于事件驱动(event-driven)的异步io(Asynchronous I/O)
       结果：
       Nginx比apache更快： Apache因IO阻塞需频繁的进程上下文切换(thread context switching),虽然单个线程(被称为轻量级进程)相对进程来说虽然上下文切换的开销虽然很小，但积少成多，大量的thread上下文切换也会造成大量cpu开销和cpu时间片的浪费。且如果apache的固定数量的thread都发生block,则apache服务器将处于长时间的空闲(idle)状态，所以降低了cpu的利用率
       Nginx比apache内存占用率更低：apache维护大量的thread需要额外的元数据和控制信息，频繁的thread上下文切换也会造成大量状态信息的保存和恢复。


MPM
   //https://httpd.apache.org/docs/2.4/en/mod/event.html
   event: 混合多进程多线程工作方式(本质还是利用单进程多线程),父进程开启负责启动多个子进程，子进程有产生由ThreadsPerChild指令指定个数的服务线程(server thread),以及一个独立的监听线程(listener thread)负责监听连接和将到底的连接转交给server thread处理。
   event的运行时配置指令与worker相同，只是额外多了一个 AsyncRequestWorkerFactor

This MPM tries to fix the 'keep alive problem' in HTTP. After a client completes the first request, it can keep the connection open, sending further requests using the same socket and saving significant overhead in creating TCP connections. However, Apache HTTP Server traditionally keeps an entire child process/thread waiting for data from the client, which brings its own disadvantages. To solve this problem, this MPM uses a dedicated listener thread for each process to handle both the Listening sockets, all sockets that are in a Keep Alive state, sockets where the handler and protocol filters have done their work and the ones where the only remaining thing to do is send the data to the client.

This new architecture, leveraging non-blocking sockets(注：这里只是non-blocking sockets而非完全是non-blocking io) and modern kernel features exposed by APR (like Linux's epoll), no longer requires the mpm-accept Mutex configured to avoid the thundering herd problem.

The total amount of connections that a single process/threads block can handle is regulated by the AsyncRequestWorkerFactor directive.



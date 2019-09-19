

https://redis.io/topics/signals#handling-of-sigsegv-sigbus-sigfpe-and-sigill




----------------------------------------------------------------------------------------------------
Handling of SIGTERM

    The SIGTERM signals tells Redis to shutdown gracefully. When this signal is received
    the server does not actually exits as a result, but it schedules a shutdown
    very similar to the one performed when the SHUTDOWN command is called.
    The scheduled shutdown starts ASAP, specifically as long as the current
    command in execution terminates (if any), with a possible additional delay of 0.1 seconds or less.

    In case the server is blocked by a Lua script that is taking too much time,
    if the script is killable with SCRIPT KILL the scheduled shutdown
    will be executed just after the script is killed, or if terminates spontaneously.

    The Shutdown performed in this condition includes the following actions:

          - If there is a background child saving the RDB file or performing an AOF rewrite, the child is killed.
          - If the AOF is active, Redis calls the fsync system call on the AOF file descriptor in order to flush the buffers on disk.
          - If Redis is configured to persist on disk using RDB files, a synchronous (blocking)
            save is performed. Since the save is performed in a synchronous way no additional memory is used.
          - If the server is daemonized, the pid file is removed.
          - If the Unix domain socket is enabled, it gets removed.
          - The server exits with an exit code of zero.

    In case the RDB file can't be saved, the shutdown fails, and the server continues to
    run in order to ensure no data loss. Since Redis 2.6.11 no further
    attempt to shut down will be made unless a new SIGTERM will be received or the SHUTDOWN command issued.



----------------------------------------------------------------------------------------------------
Handling of SIGSEGV, SIGBUS, SIGFPE and SIGILL


----------------------------------------------------------------------------------------------------
What happens when a child process gets killed



----------------------------------------------------------------------------------------------------
Killing the RDB file without triggering an error condition

    However sometimes the user may want to kill the RDB saving child without generating an error.
    Since Redis version 2.6.10 this can be done using the special signal SIGUSR1 that
    is handled in a special way: it kills the child process as any other signal,
    but the parent process will not detect this as a critical error and
    will continue to serve write requests as usually.

















To test that `mod_wsgi-express` is installed and working we have a simple WSGI hello world application. This can be found in `~/exercises/hello-world-v1/wsgi.py`.

```editor:open-file
file: ~/exercises/hello-world-v1/wsgi.py
```

To start up Apache/mod_wsgi and host this WSGI application using `mod_wsgi-express`, from the first terminal run:

```terminal:execute
command: mod_wsgi-express start-server hello-world-v1/wsgi.py --log-to-terminal
```

This should result in the output:

```
Server URL         : http://localhost:8000/
Server Root        : /tmp/mod_wsgi-localhost:8000:1001
Server Conf        : /tmp/mod_wsgi-localhost:8000:1001/httpd.conf
Error Log File     : /dev/stderr (warn)
Operating Mode     : daemon
Request Capacity   : 5 (1 process * 5 threads)
Request Timeout    : 60 (seconds)
Startup Timeout    : 15 (seconds)
Queue Backlog      : 100 (connections)
Queue Timeout      : 45 (seconds)
Server Capacity    : 20 (event/worker), 20 (prefork)
Server Backlog     : 500 (connections)
Locale Setting     : en_US.UTF-8
```

It tells you a bit about the configuration that `mod_wsgi-express` has used.

To test the WSGI application is working, in the second terminal run:

```terminal:execute
command: curl http://localhost:8000
session: 2
```

You should see the output:

```
Hello World!
```

Shutdown the server by entering `ctrl+c` into the first terminal.

```terminal:interrupt
```

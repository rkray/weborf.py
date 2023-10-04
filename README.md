Weborf py
=========

Weborf.py is a minimal webserver. This little script is inspired by the original
weborf [https://ltworf.github.io/weborf/] but doesn't implement most of its
features.

It is also abandoned.

It based on the SimpleHTTPServer but is easier to configure.

    Usage: weborf.py [options]

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  set listen port number
      -q, --quiet           don't print status messages to stdout

ToDo
====

* add an option to set the basedir. Now the current working is using.
* make listen ip configurable
* make it compatible to Mac

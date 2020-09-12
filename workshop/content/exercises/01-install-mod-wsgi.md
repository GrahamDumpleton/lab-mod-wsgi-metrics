We will be using `mod_wsgi-express`. This is a wrapper for starting up Apache/mod_wsgi which does all the configuration of Apache for you. To install it you can use `pip`.

Before we start, let's create a Python virtual environment in which to install `mod_wsgi` and any other packages we require.

To create the Python virtual environment, run:

```terminal:execute
command: python3 -m venv $HOME/venv
```

To use this Python virtual environment, you then need to activate it. Do this in all the terminals by running:

```terminal:execute-all
command: source $HOME/venv/bin/activate
```

Before we install mod_wsgi, first update the version of `pip` which is installed into the Python virtual environment. The initial version which is installed is quite often out of date, so it is always a good idea to update it to the latest version.

To update `pip`, run:

```terminal:execute
command: pip3 install -U pip
```

You can now install mod_wsgi by running:

```terminal:execute
command: pip3 install https://github.com/GrahamDumpleton/mod_wsgi/archive/develop.zip
```

This command will build and install the Apache module for `mod_wsgi` into the Python virtual environment. It will also install the `mod_wsgi-express` program.

We also need a number of other Python packages for the examples we will be running. To install these, run:

```terminal:execute
command: pip3 install -r requirements.txt
```

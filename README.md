lazy-ips
========

IPS patcher for Linux. Gtk3 and CLI user interfaces.

https://github.com/btimofeev/lazy_ips

<img src="https://github.com/btimofeev/lazy_ips/raw/master/img/screenshot.png">

Dependencies: Python3 and PyGObject

lazy-ips-cli
============

Command-line interface for IPS patching. Does not require PyGObject. Works on Linux, Windows, macOS and Android (via Termux).

Usage: ```lazy-ips-cli image_file patch_file```

Installation
------------

This step requires the `setuptools` installed on the system.

`python3 setup.py install`

This command will automatically create the necessary scripts in /usr/bin

Authors
-------

Original author: Boris Timofeev https://github.com/btimofeev  
Port to Python 3: Hubert Figuière https://github.com/hfiguiere  
Various fixes: https://github.com/hadess  
Cleanup and CLI: https://github.com/rekentuig  
Documentation and Testing: http://github.com/richardhob

Testing
-------

Testing the IPS functionality is done using Pytest:

``` bash
> python -m venv venv
> source venv/bin/activate
> python -m pip install pytest flake8
> python -m pip install -e .
> make
```

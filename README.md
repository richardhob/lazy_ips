lazy-ips
========

IPS patcher (CLI only)

Forked from:

https://github.com/btimofeev/lazy_ips

lazy-ips-cli
============

Command-line interface for IPS patching. 

Usage: ```lazy-ips-cli image_file patch_file```

Installation
------------

``` bash
> git clone http://github.com/richardhob/lazy_ips.git
> python -m pip insall ./lazy_ips
```

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

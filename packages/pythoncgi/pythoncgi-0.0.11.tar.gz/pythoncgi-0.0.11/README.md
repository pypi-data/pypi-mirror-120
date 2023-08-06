# Python CGI

<badges>[![version](https://img.shields.io/pypi/v/pythoncgi.svg)](https://pypi.org/project/pythoncgi/)
[![license](https://img.shields.io/pypi/l/pythoncgi.svg)](https://pypi.org/project/pythoncgi/)
[![pyversions](https://img.shields.io/pypi/pyversions/pythoncgi.svg)](https://pypi.org/project/pythoncgi/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Extremely simple Python CGI framework for Apache 2.</i>

# Hierarchy

```
pythoncgi
|---- _SERVER
|---- _GET
|---- _POST
|---- _SESSION
|---- _COOKIE
|---- _HEADERS
|---- set_status()
|---- set_header()
|---- execute()
|---- print()
|---- main()
|---- log_construct()
'---- log()
```

# Example
```bash
# add .py cgi handler in apache
# allow executecgi in apache
sudo nano index.py
sudo chmod +rwx index.py
```

###index.py
```python
#!/usr/bin/python3
from pythoncgi import _SERVER, _GET, _POST, _SESSION, _COOKIE, _HEADERS, set_status, set_header, execute, print, main, log_construct, flush


@execute("get")
def get():
    set_status(500)
    set_header("Cache-Control", "max-age=0, must-revalidate")
    print("_SERVER:<br>")
    print(_SERVER)
    print()
    print("_GET:<br>")
    print(_GET)
    print()
    print("_POST:<br>")
    print(_POST)
    print()
    print("_SESSION:<br>")
    print(_SESSION)
    print()
    print("_COOKIE:<br>")
    print(_COOKIE)
    print()
    print("_HEADERS:<br>")
    print(_HEADERS)
    print()
    mylogger = log_construct("mylog.log")
    mylogger("done")


if __name__ == '__main__':
    main()

```

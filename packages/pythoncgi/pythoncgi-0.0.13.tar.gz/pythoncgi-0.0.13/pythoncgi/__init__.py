__version__ = "0.0.13"
__keywords__ = ["python cgi apache"]


# if not __version__.endswith(".0"):
#     import re
#     print("version {} is deployed for automatic commitments only".format(__version__), flush=True)
#     print("install version " + re.sub(r"([0-9]+\.[0-9]+\.)[0-9]+", r"\g<1>0", __version__) + " instead")
#     import os
#     os._exit(1)


from .core import _SERVER, _GET, _POST, _SESSION, _COOKIE, _HEADERS, set_status, set_header, execute, print, main, log, log_construct


import os
import sys
import json
import datetime
import traceback as _traceback
from urllib.parse import quote, unquote
from html import escape, unescape
import http.client
from http.cookies import SimpleCookie
from cgi import FieldStorage
from omnitools import dt2yyyymmddhhmmss


default_log_file = "log.log"


if "REDIRECT_QUERY_STRING" in os.environ and not os.environ["QUERY_STRING"]:
    os.environ["QUERY_STRING"] = os.environ["REDIRECT_QUERY_STRING"]
_SERVER = dict(os.environ)
arguments = FieldStorage(environ=os.environ)
arguments = {k: [_.value for _ in arguments[k]] if isinstance(arguments[k], list) else arguments[k].value for k in arguments}
_GET = arguments
_POST = arguments
_SESSION = SimpleCookie(_SERVER["HTTP_COOKIE"]) if "HTTP_COOKIE" in _SERVER else SimpleCookie()
_COOKIE = {k: v.value for k, v in _SESSION.items()}
# need to vet it manually as it depends on the system
_HEADERS = {k: v for k, v in _SERVER.items() if k not in [
    "DOCUMENT_ROOT",
    "LANG",
    "CONTEXT_DOCUMENT_ROOT",
    "SERVER_SIGNATURE",
    "SERVER_SOFTWARE",
    "SERVER_PORT",
    "REMOTE_PORT",
    "SCRIPT_NAME",
    "SERVER_ADMIN",
    "LANGUAGE",
    "QUERY_STRING",
    "REDIRECT_QUERY_STRING",
    "GATEWAY_INTERFACE",
    "REQUEST_URI",
    "SERVER_PROTOCOL",
    "PYTHONIOENCODING",
    "SERVER_ADDR",
    "LC_ALL",
    "SCRIPT_FILENAME",
    "PATH",
    "CONTEXT_PREFIX",
]}
default_content_type = {
    "Content-Type": "text/html; charset=utf-8"
}
__headers = {}
__headers.update(default_content_type)
__response = {
    "status_code": 200,
    "content": b""
}
__methods = {}
PRINTED = {
    "STATUS": False,
    "HEADERS": False,
}


def obj_to_bytes(obj):
    if isinstance(obj, str):
        obj = obj.encode()
    elif not isinstance(obj, bytes):
        try:
            obj = json.dumps(obj, indent=2)
        except:
            obj = str(obj)
        obj = obj.encode()
    return obj


def log(obj, fp: str = None):
    obj = obj_to_bytes(obj)
    now = dt2yyyymmddhhmmss().encode()
    open(fp or default_log_file, "ab").write(now+b" "+obj+b"\n")


def log_construct(fp: str = None):
    def _log(obj):
        return log(obj, fp)

    return _log


def set_status(code: int):
    if not PRINTED["STATUS"]:
        __response["status_code"] = code
    else:
        raise Exception("! status_code printed: {}, {}".format(
            PRINTED["STATUS"],
            __response["status_code"])
        )


def set_header(k, v):
    __headers[k] = v


def flush():
    _generate_headers()
    _print(__response["content"])
    __response["content"] = b""
    sys.stdout.buffer.flush()


def _print(obj):
    sys.stdout.buffer.write(obj_to_bytes(obj))


def print(obj = "", end=b"\n"):
    __response["content"] += obj_to_bytes(obj)
    if end:
        end = obj_to_bytes(end)
        __response["content"] += end


def traceback(tag_name: str = "code", class_name: str = "traceback", style: str = "", limit=None, chain=True):
    return "<{tag} class='{}' style='{}'>{}</{tag}>".format(
        class_name,
        style,
        escape(_traceback.format_exc(limit, chain)).replace("\n", "<br>\n"),
        tag=tag_name
    )


def _generate_headers():
    session = _SESSION.output()
    if session:
        session += "\n"
    if not PRINTED["STATUS"]:
        _print("{}: {}\n".format("Status", __response["status_code"]))
        PRINTED["STATUS"] = True
    if not PRINTED["HEADERS"]:
        for k, v in __headers.items():
            _print("{}: {}\n".format(k, v))
        _print(session)
        _print("\n")
        PRINTED["HEADERS"] = True


def _generate_response():
    _generate_headers()
    content = __response["content"]
    _print(content)
    status_code = __response["status_code"]
    if not content and status_code >= 500 and status_code <= 599:
        if status_code in http.client.responses:
            msg = http.client.responses[status_code]
            status_message = "<h1>{} {}</h1><br/><p>{}</p>".format(status_code, msg, "The server has no response regarding this error.")
            _print(status_message)


def execute(method, enable_tb: bool = True, traceback_kwargs: dict = None):
    def wrapper(main):
        limit = None
        chain = True
        try:
            limit = traceback_kwargs["limit"]
        except:
            pass
        try:
            chain = traceback_kwargs["chain"]
        except:
            pass
        def _execute():
            try:
                main()
            except:
                __headers.update(default_content_type)
                log(_traceback.format_exc(limit, chain))
                if enable_tb:
                    tb = traceback(**(traceback_kwargs or {}))
                else:
                    tb = "<h1>500 Internal Server Error</h1><br/><p>HTML stack trace is disabled.<br/>Check traceback log.</p>"
                try:
                    set_status(500)
                except:
                    log(_traceback.format_exc())
                __response["content"] = tb.encode()
            try:
                _generate_response()
            except:
                try:
                    set_status(500)
                except:
                    log(_traceback.format_exc())
                log(_traceback.format_exc())

        __methods[method] = _execute
        return _execute

    return wrapper


def main():
    method = _SERVER["REQUEST_METHOD"].lower()
    if method in __methods:
        __methods[method]()
    else:
        set_status(405)


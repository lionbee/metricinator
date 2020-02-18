import os.path

_module_abs_path = os.path.abspath(os.path.dirname(__file__))
_key_path = os.path.join(_module_abs_path, "../keys")

server_config = {
    "bootstrap_servers": "some-server",
    "security_protocol": "SSL",
    "ssl_check_hostname": True,
    "ssl_cafile": os.path.join(_key_path, "ca.pem"),
    "ssl_certfile": os.path.join(_key_path, "service.cert"),
    "ssl_keyfile": os.path.join(_key_path, "service.key"),
}

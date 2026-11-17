import json, importlib.util, sys
spec = importlib.util.spec_from_file_location("ethos_check", "__init__.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert m._userkey("@ethos_network") == "service:x.com:username:ethos_network"
assert m._userkey("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045").startswith("address:0x")
assert m._userkey("bad handle!") is None
print(m.ethos_check({"subject": "not valid!!"}))
print("ok")

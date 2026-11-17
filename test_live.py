import importlib.util
spec = importlib.util.spec_from_file_location("ethos_check", "__init__.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print(m.ethos_check({"subject": "ethos_network"}))
print(m.ethos_check({"subject": "iborazzi", "min_score": 1200}))

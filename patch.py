import io
p = "__init__.py"
s = io.open(p, encoding="utf-8", newline="").read()
old = 'headers={"X-Ethos-Client": CLIENT_HEADER}'
new = 'headers={"X-Ethos-Client": CLIENT_HEADER, "User-Agent": CLIENT_HEADER, "Accept": "application/json"}'
assert old in s, "pattern not found"
io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
print("patched")

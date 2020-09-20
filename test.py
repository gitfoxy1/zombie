d = dict(a=1, b=2)

x = 0
try:
    x = d["c"]
except Exception:
    print("error")


print(x)



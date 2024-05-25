import base64

with open("theflag", "r") as f:
    d = f.readline()
    for i in range(50):
        d = base64.b64decode(d)

print(d)

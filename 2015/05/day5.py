
import hashlib


def test():
    hashlib.md5(b"abcdef609043").hexdigest()
    hashlib.md5(b"pqrstuv1048970").hexdigest()
    return 0


def find_number(key):
    n = 1
    found = False
    while not found:
        t = key + str(n)
        if hashlib.md5(t.encode("utf-8")).hexdigest()[0:5] == '00000':
            found = True
            break
        n += 1
    return n


def find_number2(key):
    n = 1
    found = False
    while not found:
        t = key + str(n)
        if hashlib.md5(t.encode("utf-8")).hexdigest()[0:6] == '000000':
            found = True
            break
        n += 1
    return n


temp = find_number("yzbqklnj")
print(f"Found value: {temp}")

temp = find_number2("yzbqklnj")
print(f"Found value: {temp}")

base = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j', 20: 'k', 21: 'l', 22: 'm', 23: 'n', 24: 'o', 25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't', 30: 'u', 31: 'v', 32: 'w', 33: 'x', 34: 'y', 35: 'z'}
def udf():
    try:
        s = int(input("Source base [2-36]: "))
        d = int(input("Destination base [2-36]: "))
        if s <= 1 or s >= 37 or d <= 1 or d >= 37:
            raise ValueError("Base limits exceeded!")
    except ValueError:raise ValueError("Invalid base entered!")
    num = input(f"Base {s} value: ")
    try:
        con = int(num,s)
        l = []
        while con > 0:
            fetch = con % d
            l.append(base.get(fetch,fetch))
            con //= d
    except ValueError:raise ValueError("Inappropriate base or wrong value entered!")
    l = list(map(str,l))
    print(f'Base {d} value:',''.join(l[::-1]))
def udf_s():
    try:
        s = int(input())
        d = int(input())
        if s <= 1 or s >= 37 or d <= 1 or d >= 37:
            raise ValueError("Base limits exceeded!")
    except ValueError:raise ValueError("Invalid base entered!")
    num = input()
    try:
        con = int(num,s)
        l = []
        while con > 0:
            fetch = con % d
            l.append(base.get(fetch,fetch))
            con //= d
    except ValueError:raise ValueError("Inappropriate base or wrong value entered!")
    l = list(map(str,l))
    print(''.join(l[::-1]))

def udt():
    try:
        s = input("Source base: ")
        d = input("Destination base: ")
        if s == "txt":
            pass
        else:
            try:
                s = int(s)
                if s <= 1 or s >= 37:
                    raise ValueError("Base limits exceeded!")
            except ValueError:
                raise ValueError("Invalid base entered!")
        if d == "txt":
            pass
        else:
            try:
                d = int(d)
                if d <= 1 or d >= 37:
                    raise ValueError("Base limits exceeded!")
            except ValueError:
                raise ValueError("Invalid base entered!")
    except ValueError:raise ValueError("Invalid base entered!")
    num = input("Value: ")

    if s != "txt" and d != "txt":
        raise TypeError("You can only to convert to or from txt using this function!")

    if s == "txt" and d != "txt":
        z = []
        l = []
        for i in num:
            z.append(ord(i))
        for i in z:
            while i > 0:
                fetch = i % d
                l.append(base.get(fetch,fetch))
                i //= d
            l.append(" ")
        l = list(map(str,l))
        cip = ''.join(l[::-1])
        cip = cip.split()
        l = cip[::-1]
        l = " ".join(l)
        hit = f"Base {d} value"

    if s != "txt" and d == "txt":
        z = []
        l = []
        for i in num.split():
            x = int(i,s)
            l.append(chr(x))
        hit = "Text"

    if s == "txt" and d == "txt":
        hit = "Text"
        l = num.split()
    
    print(f'{hit}:',''.join(l))
def udt_s():
    try:
        s = input()
        d = input()
        if s == "txt":
            pass
        else:
            try:
                s = int(s)
                if s <= 1 or s >= 37:
                    raise ValueError("Base limits exceeded!")
            except ValueError:
                raise ValueError("Invalid base entered!")
        if d == "txt":
            pass
        else:
            try:
                d = int(d)
                if d <= 1 or d >= 37:
                    raise ValueError("Base limits exceeded!")
            except ValueError:
                raise ValueError("Invalid base entered!")
    except ValueError:raise ValueError("Invalid base entered!")
    num = input()

    if s != "txt" and d != "txt":
        raise TypeError("You can only to convert to or from txt using this function!")

    if s == "txt" and d != "txt":
        z = []
        l = []
        for i in num:
            z.append(ord(i))
        for i in z:
            while i > 0:
                fetch = i % d
                l.append(base.get(fetch,fetch))
                i //= d
            l.append(" ")
        l = list(map(str,l))
        cip = ''.join(l[::-1])
        cip = cip.split()
        l = cip[::-1]
        l = " ".join(l)
        hit = f"Base {d} value"

    if s != "txt" and d == "txt":
        z = []
        l = []
        for i in num.split():
            x = int(i,s)
            l.append(chr(x))
        hit = "Text"

    if s == "txt" and d == "txt":
        hit = "Text"
        l = num.split()
    
    print(''.join(l))

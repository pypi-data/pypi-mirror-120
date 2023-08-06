def decimal_to_binary(data):
    print("Decimal value:",data)
    try:
        dec = int(data)
        bnr = bin(dec).replace('0b','')
    except ValueError:
        raise ValueError("Non-decimal value entered!")
    print("Binary value:",bnr)
def decimal_to_binary_s(data):
    try:
        dec = int(data)
        bnr = bin(dec).replace('0b','')
    except ValueError:
        raise ValueError("Non-decimal value entered!")
    print(bnr)

def decimal_to_octal(data):
    print("Decimal value:",data)
    try:
        dec = int(data)
        octal = oct(dec).replace('0o','')
    except ValueError:
        raise ValueError("Non-decimal value entered!")
    print("Octal value:",octal)
def decimal_to_octal_s(data):
    try:
        dec = int(data)
        octal = oct(dec).replace('0o','')
    except ValueError:
        raise ValueError("Non-decimal value entered!")
    print(octal)

def decimal_to_hexadecimal(data):
    print("Decimal value:",data)
    try:
        dec = int(data)
        hxd = hex(dec).replace('0x','')
    except ValueError:
        raise ValueError("Non-decimal value entered!")
    print("Hexadecimal value:",hxd)
def decimal_to_hexadecimal_s(data):
    try:
        dec = int(data)
        hxd = hex(dec).replace('0x','')
    except ValueError:
        raise ValueError("Non-decimal value entered!")
    print(hxd)

def decimal_to_text():
    data = input("Decimal value: ").split(" ")
    l = []
    for i in data:
        try:
            z = int(i)
            l.append(chr(z))
        except ValueError:
            raise ValueError("Non-decimal value entered!")
    print("ASCII value:",''.join(l))
def decimal_to_text_s():
    data = input().split(" ")
    l = []
    for i in data:
        try:
            z = int(i)
            l.append(chr(z))
        except ValueError:
            raise ValueError("Non-decimal value entered!")
    print(''.join(l))
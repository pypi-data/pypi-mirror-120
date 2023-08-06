inv = ['8','9']
def octal_to_binary(data):
    print("Octal value:",data)
    for digit in data:
        if digit in inv:
            raise ValueError("Non-octal number entered!")
        try:
            bnr = int(data,8)
            bnr = bin(bnr).replace('0b', '')
        except ValueError:
            raise ValueError("Non-octal number entered!")
    print("Binary value: ",bnr)
def octal_to_binary_s(data):
    for digit in data:
        if digit in inv:
            raise ValueError("Non-octal number entered!")
        try:
            bnr = int(data,8)
            bnr = bin(bnr).replace('0b', '')
        except ValueError:
            raise ValueError("Non-octal number entered!")
    print(bnr)

def octal_to_decimal(data):
    print("Octal value:",data)
    decimal = 0
    for i in data:
        if i in inv:
            raise ValueError("Non-octal number entered!")
        try:
            decimal = decimal*8 + int(i)
        except ValueError:
            raise ValueError("Non-octal number entered!")
    print("Decimal value:",decimal)
def octal_to_decimal_s(data):
    decimal = 0
    for i in data:
        if i in inv:
            raise ValueError("Non-octal number entered!")
        try:
            decimal = decimal*8 + int(i)
        except ValueError:
            raise ValueError("Non-octal number entered!")
    print(decimal)

def octal_to_hexadecimal(data):
    print("Octal value:",data)
    for digit in data:
        if digit in inv:
            raise ValueError("Non-octal number entered!")
        try:
            hxd = int(data,8)
            hxd = hex(hxd).replace('0x', '')
        except ValueError:
            raise ValueError("Non-octal number entered!")
    print("Hexadecimal value: ",hxd)
def octal_to_hexadecimal_s(data):
    for digit in data:
        if digit in inv:
            raise ValueError("Non-octal number entered!")
        try:
            hxd = int(data,8)
            hxd = hex(hxd).replace('0x', '')
        except ValueError:
            raise ValueError("Non-octal number entered!")
    print(hxd)

def octal_to_text():
    data = input("Octal value: ").split()
    l = []
    for i in data:
        try:
            z = int(i, 8)
            l.append(chr(z))
        except ValueError:
            raise ValueError("Non-octal number entered!")
    print("ASCII value:",''.join(l))
def octal_to_text_s():
    data = input().split()
    l = []
    for i in data:
        try:
            z = int(i, 8)
            l.append(chr(z))
        except ValueError:
            raise ValueError("Non-octal number entered!")
    print(''.join(l))
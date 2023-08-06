inv = ['2','3','4','5','6','7','8','9']
def binary_to_decimal(data):
    print("Binary value:",data)
    decimal = 0
    for digit in data:
        if digit in inv:
            raise ValueError("Non-binary number entered!")
        try:
            decimal = decimal*2 + int(digit)
        except ValueError:
            raise ValueError("Non-binary number entered!")
    print("Decimal value: ",decimal)
def binary_to_decimal_s(data):
    decimal = 0
    for digit in data:
        if digit in inv:
            raise ValueError("Non-binary number entered!")
        try:
            decimal = decimal*2 + int(digit)
        except ValueError:
            raise ValueError("Non-binary number entered!")
    print(decimal)

def binary_to_octal(data):
    print("Binary value:",data)
    for digit in data:
        if digit in inv:
            raise ValueError("Non-binary number entered!")
        try:
            octal = int(data,2)
            octal = oct(octal).replace('0o', '')
        except ValueError:
            raise ValueError("Non-binary number entered!")
    print("Octal value: ",octal)
def binary_to_octal_s(data):
    for digit in data:
        if digit in inv:
            raise ValueError("Non-binary number entered!")
        try:
            octal = int(data,2)
            octal = oct(octal).replace('0o', '')
        except ValueError:
            raise ValueError("Non-binary number entered!")
    print(octal)

def binary_to_hexadecimal(data):
    print("Binary value:",data)
    for digit in data:
        if digit in inv:
            raise ValueError("Non-binary number entered!")
        try:
            hxd = int(data,2)
            hxd = hex(hxd).replace('0x', '')
        except ValueError:
            raise ValueError("Non-binary number entered!")
    print("Hexadecimal value: ",hxd)
def binary_to_hexadecimal_s(data):
    for digit in data:
        if digit in inv:
            raise ValueError("Non-binary number entered!")
        try:
            hxd = int(data,2)
            hxd = hex(hxd).replace('0x', '')
        except ValueError:
            raise ValueError("Non-binary number entered!")
    print(hxd)

def binary_to_text():
    data = input("Binary value: ").split(" ")
    l = []
    for i in data:
        try:
            z = int(i, 2)
            l.append(chr(z))
        except ValueError:
            raise ValueError("Non-binary value entered!")
    print("ASCII value:",''.join(l))
def binary_to_text_s():
    data = input().split(" ")
    l = []
    for i in data:
        try:
            z = int(i, 2)
            l.append(chr(z))
        except ValueError:
            raise ValueError("Non-binary value entered!")
    print(''.join(l))
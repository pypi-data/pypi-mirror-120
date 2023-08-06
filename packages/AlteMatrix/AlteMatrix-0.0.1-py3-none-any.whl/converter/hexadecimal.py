def hexadecimal_to_binary(data):
    print("Hexadecimal value:",data)
    try:
        bnr = int(data,16)
        bnr = bin(bnr).replace('0b','')
    except ValueError:
        raise ValueError("Non-hexadecimal number entered!")
    print("Binary value:",bnr)
def hexadecimal_to_binary_s(data):
    try:
        bnr = int(data,16)
        bnr = bin(bnr).replace('0b','')
    except ValueError:
        raise ValueError("Non-hexadecimal number entered!")
    print(bnr)


def hexadecimal_to_octal(data):
    print("Hexadecimal value:",data)
    try:
        octal = int(data,16)
        octal = oct(octal).replace('0o','')
    except ValueError:
        raise ValueError("Non-hexadecimal number entered!")
    print("Octal value:",octal)
def hexadecimal_to_octal_s(data):
    try:
        octal = int(data,16)
        octal = oct(octal).replace('0o','')
    except ValueError:
        raise ValueError("Non-hexadecimal number entered!")
    print(octal)

def hexadecimal_to_decimal(data):
    print("Hexadecimal value:",data)
    try:
        decimal = int(data,16)
    except ValueError:
        raise ValueError("Non-hexadecimal number entered!")
    print("Decimal value:",decimal)
def hexadecimal_to_decimal_s(data):
    try:
        decimal = int(data,16)
    except ValueError:
        raise ValueError("Non-hexadecimal number entered!")
    print(decimal)

def hexadecimal_to_text():
    data = input("Hexadecimal value: ").split()
    l = []
    for i in data:
        try:
            z = chr(int(i,16))
            l.append(z)
        except ValueError:
            raise ValueError("Non-hexadecimal value entered or limit reached!")
        except OverflowError:
            raise ValueError("Hexadecimal value limit exceeded!")
    print("ASCII value:",''.join(l))
def hexadecimal_to_text_s():
    data = input().split()
    l = []
    for i in data:
        try:
            z = chr(int(i,16))
            l.append(z)
        except ValueError:
            raise ValueError("Non-hexadecimal value entered or limit reached!")
        except OverflowError:
            raise ValueError("Hexadecimal value limit exceeded!")
    print(''.join(l))
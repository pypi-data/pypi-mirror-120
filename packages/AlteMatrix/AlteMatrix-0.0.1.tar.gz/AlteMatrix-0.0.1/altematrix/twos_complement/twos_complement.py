g = {'0':'1', '1':'0'}
z = []
a = []
def com2(l,m):
    print('Value:',l)
    print('Multiplier:',m)
    print('Binary Value:',bin(l).replace('0b',''))
    b = '{:032b}'.format(m)
    print('Binary Multiplier:',b)
    for i in b:
        if i=='1':
            i = g.get(i)
            z.append(i)
        elif i=='0':
            i = g.get(i)
            z.append(i)
    x = ''.join(z)
    print('Inverse:',x)
    x = '0b'+''.join(z)
    x = int(x,2) + 1
    print('Hex Value:',hex(x))

    mul = l*m
    print('Multiplication:',mul)
    b = '{:032b}'.format(mul)
    print('Binary Multiplication:',b)
    for i in b:
        if i=='1':
            i = g.get(i)
            a.append(i)
        elif i=='0':
            i = g.get(i)
            a.append(i)
    x = ''.join(a)
    print('Inverse Multipliaction:',x)
    x = '0b'+''.join(a)
    y = x
    x = int(x,2) + 1
    x = hex(x)
    print('Hex Multiplication:',x)

def com2_s(l,m):
    b = '{:032b}'.format(m)
    for i in b:
        if i=='1':
            i = g.get(i)
            z.append(i)
        elif i=='0':
            i = g.get(i)
            z.append(i)
    x = ''.join(z)
    x = '0b'+''.join(z)
    x = int(x,2) + 1
    mul = l*m
    b = '{:032b}'.format(mul)
    for i in b:
        if i=='1':
            i = g.get(i)
            a.append(i)
        elif i=='0':
            i = g.get(i)
            a.append(i)
    x = ''.join(a)
    print(x)
    x = '0b'+''.join(a)
    y = x
    x = int(x,2) + 1
    x = hex(x)
    print(x)

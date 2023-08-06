def collatzquiet(n):
    while True:
        if n % 2 == 0:
            n = n // 2
        elif n == 1:
            break
        elif n % 2 == 1:
            n = 3 * n + 1
        
        elif n == 1:
            break
    print(str(n))
    return n

def collatz(n):
    while True:
        if n % 2 == 0:
            print(str(n))
            n = n // 2
        elif n == 1:
            break
        elif n % 2 == 1:
            print(str(n))
            n = 3 * n + 1
        
        elif n == 1:
            break
    print(str(n))
    return n
def collatzextra(n):
    print(str(n))
    while True:
        if n % 2 == 0:
            print('// 2')
            n = n // 2
            print (str(n))
        elif n == 1:
            break
        elif n % 2 == 1:
            print(' * 3 + 1')
            n = 3 * n + 1
        
        elif n == 1:
            return n
            break
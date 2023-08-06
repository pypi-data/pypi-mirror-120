def collatz(n):
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

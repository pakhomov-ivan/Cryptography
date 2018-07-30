import random as rand
import time
from Elliptic_Curve import gcdex

'''
Prime_number(n)
функция возвращает список простых чисел от m до n
'''
def Prime_numbers(m, n):
    a = list(range(n + 1))
    a[1] = 0
    lst = list()
    i = 2
    while i <= n:
        if a[i] != 0:
            lst.append(a[i])
            for j in range(i**2, n + 1, i):
                a[j] = 0
        i += 1
    return [i for i in lst if i > m]

def isPrime(N):
    if N == 2:
        return True
    for i in range(100):
        n = rand.randint(2, N-2)
        if gcdex(N, n)[0] != 1:
            return False
        if pow(n, N-1, N) != 1: #тест Ферма
            return False
    return True

'''
Функция Эйлера phi(n)
'''
def Euler_phi(n):
    result = n
    i = 2
    while i**2 <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result//i
        i += 1
    if n > 1:
        result -= result//n
    return result

'''
Первообразный корень g от m это:
g^phi(m) % m = 1 и g^L % m != 1,
где 1 <= L < phi(m)
phi(m) - функция Эйлера
'''
def Primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1
    while True:
        g = rand.randint(2, p - 1)
        if not pow(g, (p - 1) // p1, p) == 1:
            if not pow(g, (p - 1) // p2, p) == 1:
                return g

'''
Класс криптосистемы Эльгамаля
'''
class Elgamal:
    def __init__(self, length_of_key):
        #self.prime = rand.choice(Prime_numbers(2003, 55296))
        '''на 2003 заканчиваются русские символы. после 55296 начинаются суррогатные пары, которые запрещены'''
        #self.prime = 6277101735386680763835789423207666416083908700390324961279
        while True:
            self.prime = rand.getrandbits(length_of_key)
            if isPrime(self.prime):
                print("Done!")
                break
        self.alpha = Primitive_root(self.prime)
        self.private = rand.randint(2, self.prime - 1)
        self.betta = pow(self.alpha, self.private, self.prime)

    def Encrypt(self, mes):
        session_key = rand.randint(2, self.prime - 1)
        C1 = pow(self.alpha, session_key, self.prime)
        C2 = mes * pow(self.betta, session_key, self.prime) % self.prime
        return C1, C2

    def Decrypt(self, C1, C2):
        return C2 * pow(C1, self.prime - 1 - self.private, self.prime) % self.prime

if __name__ == '__main__':
    encode = 'utf-16'
    text = open('text.txt', 'rt', encoding=encode)
    crypt = open('Crypt.txt', 'wt', encoding=encode)
    decrypt = open('Decrypt.txt', 'wt', encoding=encode)
    length_of_key = 1024
    mashine = Elgamal(length_of_key)

    time_to_encrypt = 0
    time_to_decrypt = 0

    for line in text.readlines():
        for symbol in line:
            symbol = ord(symbol)
            start = time.time()
            enc_symbol = mashine.Encrypt(symbol)
            time_to_encrypt += time.time() - start
            for i in enc_symbol:
                crypt.write(str(hex(i)))
    crypt.close()

    crypt = open('Crypt.txt', 'rt', encoding=encode)
    cry = crypt.read().split('0x')
    for i in range(1, len(cry), 2):
        C1, C2 = int(cry[i], 16), int(cry[i+1], 16)
        start = time.time()
        dec_symbol = mashine.Decrypt(C1, C2)
        time_to_decrypt += time.time() - start
        decrypt.write(chr(dec_symbol))

    print("---Encrypt for %s seconds---" % time_to_encrypt)
    print("---Decrypt for %s seconds---" % time_to_decrypt)
    decrypt.write('\n\n---Classic Elgamal---')
    decrypt.write('\n---Length of key %s bits---' % length_of_key)
    decrypt.write("\n---Encrypt for %s seconds---" % time_to_encrypt)
    decrypt.write("\n---Decrypt for %s seconds---" % time_to_decrypt)
    crypt.close()
    decrypt.close()
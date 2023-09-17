#!/usr/bin/env python3

from codetiming import Timer

def main():
    t = Timer()
    number = (int(input("Enter the number up to which you want to spot the primes: ")))

    prime_list = []
    t.start()
    for n in range(number):
        if is_prime(n):
            prime_list.append(n)
    print(prime_list, file=open('output.txt', 'w'))
    print(f"There are {len(prime_list)} prime numbers up to {number}. Using the new function")
    t.stop()

    prime_list = []
    t.start()
    for n in range(number):
        if is_prime_old(n):
            prime_list.append(n)
    # print(prime_list)
    print(f"There are {len(prime_list)} prime numbers up to {number}. Using the old function")
    t.stop()


def is_prime_old(number):
    for i in range(2, number):
        if number % i == 0:
            return False
            break
    else:
        return True

def is_prime(number):
    if number <= 0:
        return False
    elif number <= 3:
        return True
    elif number % 2 == 0:
        return False
    else:

        sqrt_num = int(number ** 0.5) + 1
        for i in range(3, sqrt_num, 2):
            if number % i == 0:
                return False
                break
        else:
            return True

if __name__ == "__main__":
    main()
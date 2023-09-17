#!/usr/bin/env python3

from codetiming import Timer
import prime

def main():
    t = Timer()
    number = (int(input("Enter the number up to which you want to spot the primes: ")))

    prime_list = []
    t.start()
    for n in range(number):
        if prime.is_prime(n):
            prime_list.append(n)
    print(prime_list, file=open('./output.txt', 'w'))
    print(f"There are {len(prime_list)} prime numbers up to {number}. Using the new function")
    t.stop()

    prime_list = []
    t.start()
    for n in range(number):
        if prime.is_prime_GPT(n):
            prime_list.append(n)
    # print(prime_list)
    print(f"There are {len(prime_list)} prime numbers up to {number}. Using the GPT function")
    t.stop()

    prime_list = []
    t.start()
    for n in range(number):
        if prime.is_prime_old(n):
            prime_list.append(n)
    # print(prime_list)
    print(f"There are {len(prime_list)} prime numbers up to {number}. Using the old function")
    t.stop()


if __name__ == "__main__":
    main()
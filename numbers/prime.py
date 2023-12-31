#!/usr/bin/env python3

def main():
    num = int(input("Enter a number: "))

    print("using optimized function:")
    if is_prime(num):
        print(f"{num} is prime")
    else:
        print (f"{num} is not prime")

    print("using original function:")
    if is_prime_old(num):
        print(f"{num} is prime")
    else:
        print (f"{num} is not prime")

    print("using GPT function:")
    if is_prime_GPT(num):
        print(f"{num} is prime")
    else:
        print (f"{num} is not prime")

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

def is_prime_old(number):
    for i in range(2, number):
        if number % i == 0:
            return False
            break
    else:
        return True

def is_prime_GPT(number):
    # proposed by chatGPT
    if number <= 1:
        return False
    elif number <= 3:
        return True
    elif number % 2 == 0 or number % 3 == 0:
        return False
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True

if __name__ == "__main__":
    main()
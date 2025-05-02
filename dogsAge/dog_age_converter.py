# https://chatgpt.com/share/68132b11-28d8-800c-a5e2-465f3141a89e

import math

def maltipoo_to_human_age(dog_age):
    """
    Convert Maltipoo (small dog) age to human-equivalent years using adjusted logarithmic model.
    
    Parameters:
        dog_age (float): Age of the Maltipoo in years.
    
    Returns:
        float: Estimated human-equivalent age.
    """
    if dog_age <= 0:
        raise ValueError("Dog age must be greater than 0.")
    if dog_age <= 2:
        return 16 * math.log(dog_age) + 31
    else:
        return 16 * math.log(dog_age) + 29  # 31 - 2 correction for small breeds

# da = float(input("enter your dog's age: "))
# print("Your dog's age in human years is: ", maltipoo_to_human_age(da))

try:
    dog_age = float(input("Enter your Maltipoo's age in years: "))
    human_age = maltipoo_to_human_age(dog_age)
    print(f"A {dog_age:.1f}-year-old Maltipoo is approximately {human_age:.1f} human years old.")
except ValueError as e:
    print(f"Invalid input: {e}")
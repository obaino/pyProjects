
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

da = float(input("enter your dog's age: "))
print("Your dog's age in human years is: ", maltipoo_to_human_age(da))
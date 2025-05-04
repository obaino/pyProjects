def look_and_say(n):
    """Generate the first n terms of the Look-and-Say sequence."""
    if n <= 0:
        return []
    
    sequence = ["1"]
    
    for _ in range(1, n):
        prev = sequence[-1]
        next_term = ""
        count = 1
        
        for i in range(1, len(prev)):
            if prev[i] == prev[i - 1]:
                count += 1
            else:
                next_term += str(count) + prev[i - 1]
                count = 1
        next_term += str(count) + prev[-1]  # Add the last group
        sequence.append(next_term)
    
    return sequence

# Example: Generate the first 10 terms
for i, term in enumerate(look_and_say(10), start=1):
    print(f"{i}: {term}")
